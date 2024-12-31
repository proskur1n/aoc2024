package main

import (
	"fmt"
	"os"
	"slices"
)

type hardDrive []uint8

func toHardDrive(bytes []byte) hardDrive {
	hd := slices.Clone(bytes)
	for i, b := range hd {
		hd[i] = b - '0'
	}
	return hd
}

func (hd hardDrive) lastFile() pointer {
	return pointer(len(hd) - 1 + (len(hd)-1)%2)
}

type pointer int

func (p pointer) isFile() bool {
	return p%2 == 0
}

func (p pointer) fileId() int {
	if !p.isFile() {
		panic("Only files have IDs")
	}
	return int(p / 2)
}

func main() {
	bytes, err := os.ReadFile("input")
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to read file", err)
		os.Exit(1)
	}
	if len(bytes) > 0 && bytes[len(bytes)-1] == '\n' {
		bytes = bytes[:len(bytes)-1]
	}

	hd := toHardDrive(bytes)

	// Part One
	{
		remaining := slices.Clone(hd)
		checksum := 0
		writePos := 0
		i := pointer(0)
		j := hd.lastFile() // Always points to a file

		for i <= j {
			if i.isFile() {
				size := remaining[i]
				for range size {
					checksum += i.fileId() * writePos
					writePos++
				}
				i++
			} else {
				copied := min(remaining[i], remaining[j])
				for range copied {
					checksum += j.fileId() * writePos
					writePos++
				}
				remaining[i] -= copied
				if remaining[i] == 0 {
					i++
				}
				remaining[j] -= copied
				if remaining[j] == 0 {
					// Step back to the previous file.
					j -= 2
				}
			}
		}

		fmt.Println(checksum)
	}

	// Part Two
	{
		prefixSum := make([]int, len(hd))
		for i := 0; i < len(hd)-1; i++ {
			prefixSum[i+1] = prefixSum[i] + int(hd[i])
		}
		remaining := slices.Clone(hd)
		checksum := 0
		j := hd.lastFile() // Always points to a file

		for j >= 0 {
			i := pointer(1)
			for i < j {
				if hd[j] <= remaining[i] {
					break
				}
				i += 2 // Step forward to the next possibly free space.
			}
			var writePos int
			if i < j {
				// Move file to region i.
				writePos = prefixSum[i] + int(hd[i]-remaining[i])
				remaining[i] -= hd[j]
			} else {
				// File stays where it is now.
				writePos = prefixSum[j]
			}
			for range hd[j] {
				checksum += j.fileId() * writePos
				writePos++
			}
			// Step back to the previous file.
			j -= 2
		}

		fmt.Println(checksum)
	}
}
