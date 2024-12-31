import Control.Monad (guard)
import Data.Text (pack, unpack, stripSuffix)
import Data.Maybe (mapMaybe)
import Text.Read (readMaybe)

type Result = Integer
type Operand = Integer

data Equation = Equation Result [Operand] deriving Show

-- Returns a value X such that X (+) operand = result
type InverseOperation = Result -> Operand -> Maybe Result

addition :: InverseOperation
addition result operand
  = guard (result >= operand) >> Just (result - operand)

multiplication :: InverseOperation
multiplication result operand
  = guard (result `mod` operand == 0) >> Just (result `div` operand)

concatenation :: InverseOperation
concatenation result operand
  = stripSuffix (pack $ show operand) (pack $ show result) >>= readMaybe . unpack

feasible :: [InverseOperation] -> Equation -> Bool
feasible ops (Equation target operands) = feasible' (reverse operands) target
  where
    feasible' [operand] target
      = target == operand
    feasible' (operand:operands) target
      = any (feasible' operands) $ mapMaybe (\op -> op target operand) ops
    feasible' [] _
      = False

calibrationResult :: [InverseOperation] -> [Equation] -> Integer
calibrationResult ops = sum . map (\(Equation target _) -> target) . filter (feasible ops)

main :: IO ()
main = do
  equations <- map parse . lines <$> readFile "input"
  print $ calibrationResult [addition, multiplication] equations
  print $ calibrationResult [addition, multiplication, concatenation] equations
  where
    parse line =
      let (target:operands) = words line
      in Equation (read $ init target) (map read operands)
