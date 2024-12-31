package main

import (
	"bufio"
	"fmt"
	"os"
	"runtime"
	"slices"
)

type direction int

const (
	up direction = iota
	right
	down
	left
)

type plan struct {
	sketch [][]byte
	w, h   int
	x, y   int
	dir    direction
}

func parse(filePath string) (plan, error) {
	file, err := os.Open(filePath)
	if err != nil {
	}
	defer file.Close()

	var sketch [][]byte

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		sketch = append(sketch, slices.Clone(scanner.Bytes()))
	}
	if err := scanner.Err(); err != nil {
	}

	width, height := len(sketch[0]), len(sketch)

	var posX, posY int
outer:
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			switch rune(sketch[y][x]) {
			case '^', '>', 'v', '<':
				posX, posY = x, y
				break outer
			}
		}
	}

	var dir direction
	switch sketch[posY][posX] {
	case '^':
		dir = up
	case '>':
		dir = right
	case 'v':
		dir = down
	case '<':
		dir = left
	}

	return plan{sketch: sketch, w: width, h: height, x: posX, y: posY, dir: dir}, nil
}

func (p *plan) copy() plan {
	sketch := make([][]byte, 0, len(p.sketch))

	for _, row := range p.sketch {
		sketch = append(sketch, slices.Clone(row))
	}

	copy := *p
	copy.sketch = sketch
	return copy
}

type position struct {
	x, y int
}

func (p *plan) patrol() (loop bool, visitedFields []position) {
	type state struct {
		x, y int
		dir  direction
	}

	x, y := p.x, p.y
	dir := p.dir
	visited := make([]uint8, p.w*p.h)
	var cycle bool

	for {
		if visited[y*p.w+x]&(1<<dir) != 0 {
			cycle = true
			break
		}
		visited[y*p.w+x] |= (1 << dir)

		nextX, nextY := x, y
		switch dir {
		case up:
			nextY -= 1
		case right:
			nextX += 1
		case down:
			nextY += 1
		case left:
			nextX -= 1
		}

		if !(nextX >= 0 && nextX < p.w && nextY >= 0 && nextY < p.h) {
			cycle = false
			break
		}
		if p.sketch[nextY][nextX] == '#' {
			dir = (dir + 1) % 4
		} else {
			x, y = nextX, nextY
		}
	}

	for y := 0; y < p.h; y++ {
		for x := 0; x < p.w; x++ {
			if visited[y*p.w+x] != 0 {
				visitedFields = append(visitedFields, position{x, y})
			}
		}
	}
	return cycle, visitedFields
}

func main() {
	plan, err := parse("input")
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to read input", err)
	}

	_, visited := plan.patrol()
	fmt.Println("Part One:", len(visited))

	workers := runtime.NumCPU()
	workSize := (len(visited) + workers - 1) / workers
	results := make(chan int, workers)

	for i := range workers {
		go func(i int) {
			plan := plan.copy()

			begin := i * workSize
			end := min(len(visited), (i+1)*workSize)

			count := 0

			for k := begin; k < end; k++ {
				x, y := visited[k].x, visited[k].y
				if x == plan.x && y == plan.y {
					continue
				}
				c := plan.sketch[y][x]
				plan.sketch[y][x] = '#'
				loop, _ := plan.patrol()
				if loop {
					count++
				}
				plan.sketch[y][x] = c
			}

			results <- count
		}(i)
	}

	total := 0
	for range workers {
		count := <-results
		total += count
	}
	fmt.Println("Part Two:", total)
}
