from abc import ABC, abstractmethod
from typing import List

from general.utils import read_lines


class IProblemSolver(ABC):
    def __init__(self,
                 input_file_name: str = "input.txt",
                 smaller_input_file_name: str = "smaller_input.txt",
                 use_smaller_input: bool = False,
                 ):
        if use_smaller_input:
            self.input_file_name = smaller_input_file_name
        else:
            self.input_file_name = input_file_name

    def solve(self):
        lines = read_lines(self.input_file_name)
        return {
            "solution_part_1": self.solve_part_1(lines),
            "solution_part_2": self.solve_part_2(lines),
        }

    @abstractmethod
    def solve_part_1(self, lines: List[str]):
        pass

    @abstractmethod
    def solve_part_2(self, lines: List[str]):
        pass
