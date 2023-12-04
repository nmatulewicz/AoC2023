import math
from typing import List

from general.problem_solver_interface import IProblemSolver


class Card:
    def __init__(self,
                 winning_numbers: List[int],
                 my_numbers: List[int],
                 ):
        self.winning_numbers = winning_numbers
        self.my_numbers = my_numbers

    def calculate_points(self):
        overlapping_number_count = self.count_overlapping_numbers()
        if overlapping_number_count > 0:
            return math.pow(2, overlapping_number_count-1)
        return 0

    def count_overlapping_numbers(self):
        overlapping_numbers = [number for number in self.my_numbers if number in self.winning_numbers]
        return len(overlapping_numbers)

    @staticmethod
    def from_line(line: str):
        number_part = line.split(":")[1]
        [winning_numbers_part, my_numbers_part] = number_part.split("|")
        return Card(
            winning_numbers=Card._read_numbers(winning_numbers_part),
            my_numbers=Card._read_numbers(my_numbers_part),
        )

    @staticmethod
    def _read_numbers(space_separated_string: str) -> List[int]:
        space_separated_string = space_separated_string.replace("  ", " ").removeprefix(" ").removesuffix(" ")
        number_strings = space_separated_string.split(" ")
        numbers = [int(number_string) for number_string in number_strings]
        return numbers


class ProblemSolverDay4(IProblemSolver):

    def solve_part_1(self, lines: List[str]):
        cards = [Card.from_line(line) for line in lines]
        points = [card.calculate_points() for card in cards]
        return sum(points)

    def solve_part_2(self, lines: List[str]):
        cards = [Card.from_line(line) for line in lines]
        number_of_copies = [1] * len(cards)
        for i, card in enumerate(cards):
            overlapping_numbers_count = card.count_overlapping_numbers()
            for j in range(i+1, i+1+overlapping_numbers_count):
                number_of_copies[j] += number_of_copies[i]
        return sum(number_of_copies)


if __name__ == '__main__':
    print(ProblemSolverDay4(use_smaller_input=True).solve())
    print(ProblemSolverDay4(use_smaller_input=False).solve())
