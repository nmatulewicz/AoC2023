from typing import List

from general.problem_solver_interface import IProblemSolver
from general.utils import try_parse_int


class ProblemSolverDay3(IProblemSolver):

    def solve_part_2(self, lines: List[str]):
        array = ProblemSolverDay3.lines_to_array(lines)
        numbers = ArrayHelper.get_numbers(array)
        stars = ArrayHelper.get_stars(array)
        total = 0
        for star in stars:
            gear_ratio, success = star.try_get_gear_ration(numbers)
            if success:
                total += gear_ratio
        return total

    def solve_part_1(self, lines: List[str]):
        array = ProblemSolverDay3.lines_to_array(lines)
        numbers = ArrayHelper.get_numbers(array)
        numbers_filtered = [number for number in numbers if number.touches_symbol()]
        return sum([array_number.value for array_number in numbers_filtered])

    @staticmethod
    def lines_to_array(lines: List[str]) -> List[List[str]]:
        return [list(line) for line in lines]


class ArrayNumber:

    def __init__(self,
                 value: int,
                 row: int,
                 col_start: int,
                 col_end: int,
                 array: List[List[str]],
                 ):
        self.value = value
        self.row = row
        self.col_start = col_start
        self.col_end = col_end
        self.array = array

    def touches_symbol(self) -> bool:
        for row in [self.row - 1, self.row, self.row + 1]:
            for col in range(self.col_start - 1, self.col_end + 2):
                if 0 <= row < len(self.array) and 0 <= col < len(self.array[row]):
                    if ArrayHelper.contains_symbol(self.array, row, col):
                        return True
        return False

    def __str__(self):
        return str(self.value)


class ArrayStar:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def try_get_gear_ration(self, numbers: List[ArrayNumber]):
        touching_numbers = [number for number in numbers if self.is_touching(number)]
        if len(touching_numbers) != 2:
            return None, False
        gear_ratio = touching_numbers[0].value * touching_numbers[1].value
        return gear_ratio, True

    def is_touching(self, array_number: ArrayNumber) -> bool:
        return (array_number.row - 1 <= self.row <= array_number.row + 1) \
            and (array_number.col_start - 1 <= self.col <= array_number.col_end + 1)


class ArrayHelper:
    @staticmethod
    def contains_symbol(array: List[List[str]], row: int, col: int):
        entry = array[row][col]
        _, success = try_parse_int(entry)
        if success:
            return False
        else:
            return entry != "."

    @staticmethod
    def get_numbers(array: List[List[str]]) -> List[ArrayNumber]:
        numbers: List[ArrayNumber] = []
        for row in range(len(array)):
            col = 0
            while col < len(array[row]):
                entry = array[row][col]
                value, success = try_parse_int(entry)
                if not success:
                    col += 1
                    continue
                start_col = col
                number = value
                while success:
                    col += 1
                    if col < len(array[row]):
                        entry = array[row][col]
                        value, success = try_parse_int(entry)
                    else:
                        success = False
                    if not success:
                        numbers.append(ArrayNumber(
                            value=number,
                            row=row,
                            col_start=start_col,
                            col_end=col-1,
                            array=array,
                        ))
                        continue
                    number = 10 * number + value
        return numbers

    @staticmethod
    def get_stars(array: List[List[str]]) -> List[ArrayStar]:
        stars: List[ArrayStar] = []
        for row in range(len(array)):
            for col in range(len(array[row])):
                entry = array[row][col]
                if entry == "*":
                    stars.append(ArrayStar(row=row, col=col))
        return stars


if __name__ == '__main__':
    # result = ProblemSolverDay3(use_smaller_input=True).solve()
    result = ProblemSolverDay3(use_smaller_input=False).solve()
    print(result)
