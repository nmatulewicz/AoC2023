import attr
import numpy as np
import time
from enum import StrEnum
from typing import List, Tuple

from general.problem_solver_interface import IProblemSolver


@attr.dataclass
class Position(StrEnum):
    ROUND_ROCK = "O"
    CUBE_SHAPED_ROCK = "#"
    EMPTY_SPACE = "."


def lines_to_array(lines: List[str]) -> np.ndarray:
    return np.array([[char for char in line] for line in lines], str)


def try_move_to_north(row_index: int, column_index: int, field: np.ndarray):
    entry = field[row_index][column_index]
    if entry != "O" or row_index == 0:
        return

    northern_neighbouring_entry = field[row_index-1][column_index]
    if northern_neighbouring_entry != ".":
        return

    field[row_index, column_index], field[row_index-1, column_index] = \
        field[row_index-1, column_index], field[row_index, column_index]
    return try_move_to_north(row_index-1, column_index, field)


def slide_rocks_to_north(field: np.ndarray):
    row_count, col_count = field.shape
    for row_index in range(row_count):
        for col_index in range(col_count):
            try_move_to_north(row_index, col_index, field)


def complete_cycle(field: np.ndarray):
    for _ in range(4):
        slide_rocks_to_north(field)
        field = np.rot90(field, 3)
    return field


def smarter_slide_rocks_to_north(field: np.ndarray):
    # print("before transpose: \n", field)
    # transposed_field = field.transpose()
    # print("after transpose: \n", transposed_field)
    # smarter_slide_rocks_to_west(transposed_field)
    row_count, col_count = field.shape


def count_points(field: np.ndarray):
    row_count = field.shape[0]
    total_points = 0
    for row_index in range(row_count):
        points_per_round_rock = row_count - row_index
        field_row: np.array = field[row_index]
        rock_count = (field_row == "O").sum()
        points = rock_count * points_per_round_rock
        total_points += points
    return total_points


class ProblemSolver(IProblemSolver):

    def solve_part_1(self):
        field = lines_to_array(self.lines)
        slide_rocks_to_north(field)
        return count_points(field)

    N_CYCLES = 1_000_000_000
    def solve_part_2(self, n_cycles=100):
        print("part 2")
        field = lines_to_array(self.lines)
        repetitive_cycle_was_found = False
        start_time = time.time()
        found_fields_per_score: dict[int, List[Tuple[np.ndarray, int]]] = {}  # dict(points, list[(field, cycle_number)]
        for cycle in range(1, 1000):
            if repetitive_cycle_was_found:
                break
            field = complete_cycle(np.copy(field))
            score = count_points(field)
            print(f"score: {score}, cycle: {cycle}")
            found_field_and_cycle_tuples = found_fields_per_score.get(score, [])
            for found_field, found_field_cycle in found_field_and_cycle_tuples:
                if np.array_equal(found_field, field):
                    repetitive_cycle_was_found = True
                    start_first_repetitive_cycle = found_field_cycle
                    start_second_repetitive_cycle = cycle
                    break
            if not repetitive_cycle_was_found:
                found_field_and_cycle_tuples.append((field, cycle))
                found_fields_per_score[score] = found_field_and_cycle_tuples

        if not repetitive_cycle_was_found:
            raise Exception("No repetitive cycle was found")

        repetitive_cycle_length = start_second_repetitive_cycle - start_first_repetitive_cycle
        number_of_remaining_cycles = ((n_cycles - start_first_repetitive_cycle) % repetitive_cycle_length)
        cycle_number_of_millionth_field = start_first_repetitive_cycle + number_of_remaining_cycles
        for my_tuple in [my_tuple for tuples in found_fields_per_score.values() for my_tuple in tuples]:
            field, cycle_count = my_tuple
            if cycle_count == cycle_number_of_millionth_field:
                millionth_field = field
                break

        end_time = time.time()
        time_delta = end_time - start_time
        print(f"time elapsed: {time_delta} s")
        return count_points(millionth_field)


if __name__ == '__main__':
    print(ProblemSolver(use_smaller_input=True).solve())
    print(ProblemSolver(use_smaller_input=False).solve())