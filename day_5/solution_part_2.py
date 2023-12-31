from copy import copy
from typing import List, Optional

import attr

from day_5.solution import ProblemSolverDay5
from general.problem_solver_interface import IProblemSolver
from general.utils import read_file

@attr.dataclass
class Range:
    start: int
    end: int

    def __attrs_post_init__(self):
        # Ensure that start is less than or equal to end
        if self.start > self.end:
            raise ValueError("Start must be less than or equal to end")

    def try_combine_with(self, other: 'Range') -> Optional['Range']:
        if not self.overlaps_with(other):
            return None
        combined_start = min(self.start, other.start)
        combined_end = max(self.end, other.end)
        return Range(combined_start, combined_end)

    def overlaps_with(self, other: 'Range') -> bool:
        return self.start <= other.end + 1 and other.start <= self.end + 1

    def without(self,
                smaller_range: Optional['Range']=None,
                greater_range: Optional['Range']=None
                ) -> Optional['Range']:
        res = copy(self)
        if smaller_range is not None:
            if smaller_range.end >= res.end:
                return None
            else:
                res.start = max(smaller_range.end + 1, res.start)
        if greater_range is not None:
            if greater_range.start <= res.start:
                return None
            else:
                res.end = min(greater_range.start - 1, res.end)
        if res.end < res.start:
            return None
        return res

    def __copy__(self):
        return Range(self.start, self.end)


@attr.dataclass
class SortedRangeList:
    sorted_ranges: List[Range]

    def add(self, range_to_add: Range):

        first_possibly_overlapping_range = next((old_range for old_range in self.sorted_ranges
                                                if old_range.end + 1 >= range_to_add.start), None)
        if first_possibly_overlapping_range is None:
            self.sorted_ranges.append(range_to_add)
            return

        possibly_overlapping_range = first_possibly_overlapping_range
        index_possibly_overlapping_range = self.sorted_ranges.index(first_possibly_overlapping_range)
        combined_range = possibly_overlapping_range.try_combine_with(range_to_add)
        while combined_range is not None:
            overlapping_range = self.sorted_ranges[index_possibly_overlapping_range]
            self.sorted_ranges.remove(overlapping_range)
            range_to_add = combined_range
            if index_possibly_overlapping_range >= len(self.sorted_ranges):
                break
            possibly_overlapping_range = self.sorted_ranges[index_possibly_overlapping_range]
            combined_range = possibly_overlapping_range.try_combine_with(range_to_add)
        self.sorted_ranges.insert(index_possibly_overlapping_range, range_to_add)

    def __len__(self):
        return len(self.sorted_ranges)

    def __getitem__(self, index):
        return self.sorted_ranges[index]


@attr.dataclass
class MapFunc:
    valid_input_range: Range
    delta: int

    def map(self, source_range: Range) -> Range:
        calculation_range_start = max(self.valid_input_range.start, source_range.start)
        calculation_range_end = min(self.valid_input_range.end, source_range.end)
        return Range(
            start=calculation_range_start + self.delta,
            end=calculation_range_end + self.delta,
        )

    @staticmethod
    def from_line(line: str) -> 'MapFunc':
        dst, src, rng = line.split(" ")
        start = int(src)
        end = start + int(rng) - 1
        delta = int(dst) - start
        return MapFunc(
            valid_input_range=Range(start=int(src), end=end),
            delta=delta
        )


@attr.dataclass
class RangeMapper:
    sorted_map_funcs: List[MapFunc]

    def map(self, source_ranges: SortedRangeList):
        destination_ranges = SortedRangeList([])

        current_source_range_index = 0
        current_source_range = source_ranges[current_source_range_index]
        remaining_source_range = copy(current_source_range)

        current_map_func_index = 0

        while current_map_func_index < len(self.sorted_map_funcs):
            current_map_func = self.sorted_map_funcs[current_map_func_index]
            while remaining_source_range.end < current_map_func.valid_input_range.start:
                destination_ranges.add(remaining_source_range)
                current_source_range_index += 1
                if current_source_range_index >= len(source_ranges):
                    destination_ranges.add(remaining_source_range)
                    return destination_ranges
                current_source_range = source_ranges[current_source_range_index]
                remaining_source_range = copy(current_source_range)
            if remaining_source_range.start < current_map_func.valid_input_range.start:
                unmappable_range_part = \
                    Range(start=remaining_source_range.start, end=current_map_func.valid_input_range.start-1)
                destination_ranges.add(unmappable_range_part)
                remaining_source_range = Range(
                    start=unmappable_range_part.end+1,
                    end=remaining_source_range.end,
                )
            remaining_source_range_overlaps_with_current_func_map = \
                current_map_func.valid_input_range.end >= remaining_source_range.start \
                and remaining_source_range.end >= current_map_func.valid_input_range.start
            if remaining_source_range_overlaps_with_current_func_map:
                destination_ranges.add(current_map_func.map(remaining_source_range))
                remaining_source_range = remaining_source_range.without(current_map_func.valid_input_range)
                if remaining_source_range is None:
                    current_source_range_index += 1
                    if current_source_range_index >= len(source_ranges):
                        return destination_ranges
                    current_source_range = source_ranges[current_source_range_index]
                    remaining_source_range = copy(current_source_range)
                    continue
            if remaining_source_range.end > current_map_func.valid_input_range.end:
                remaining_source_range = \
                    Range(
                        start=max(current_map_func.valid_input_range.end + 1, remaining_source_range.start),
                        end=remaining_source_range.end
                    )
            current_map_func_index += 1
        destination_ranges.add(remaining_source_range)
        current_source_range_index += 1
        while current_source_range_index < len(source_ranges):
            current_source_range = source_ranges[current_source_range_index]
            destination_ranges.add(current_source_range)
            current_source_range_index += 1
        return destination_ranges

    @staticmethod
    def from_lines(lines: List[str]) -> 'RangeMapper':
        lines = lines[1:]
        func_maps = [MapFunc.from_line(line) for line in lines]
        sorted_func_maps = sorted(func_maps, key=lambda func_map: func_map.valid_input_range.start)
        return RangeMapper(sorted_func_maps)


def get_seed_ranges(seeds_str: str) -> SortedRangeList:
    numbers = ProblemSolverDay5.get_seeds_part_1(seeds_str)
    seed_ranges = SortedRangeList([])
    for i in range(0, len(numbers), 2):
        start = numbers[i]
        length = numbers[i + 1]
        seed_ranges.add(Range(start, start + length - 1))
    return seed_ranges


def get_source_destination_mappers(mappers_part: str) -> List[RangeMapper]:
    sd_mappers: List[RangeMapper] = []
    mapper_strings = mappers_part.split("\n\n")
    for string in mapper_strings:
        sd_mappers.append(RangeMapper.from_lines(string.splitlines()))
    return sd_mappers


def find_location_ranges(seed_range_collection: SortedRangeList, range_mappers: List[RangeMapper]):
    source_ranges = seed_range_collection
    for mapper in range_mappers:
        destination_range = mapper.map(source_ranges)
        source_ranges = destination_range
    return source_ranges


def get_range_mappers(mappers_part: str):
    range_mappers: List[RangeMapper] = []
    mapper_strings = mappers_part.split("\n\n")
    for string in mapper_strings:
        range_mappers.append(RangeMapper.from_lines(string.splitlines()))
    return range_mappers


class ProblemSolver(IProblemSolver):

    def solve_part_1(self):
        pass

    def solve_part_2(self):
        input_str = read_file(self.input_file_name)
        seeds_part, mappers_part = input_str.split("\n\n", 1)
        seed_ranges = get_seed_ranges(seeds_part)
        range_mappers = get_range_mappers(mappers_part)
        final_destination_ranges = find_location_ranges(seed_ranges, range_mappers)
        return final_destination_ranges.sorted_ranges[0].start


if __name__ == '__main__':
    print(ProblemSolver(use_smaller_input=True).solve())
    print(ProblemSolver(use_smaller_input=False).solve())
