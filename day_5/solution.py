from typing import List, Iterator, Optional

from general.problem_solver_interface import IProblemSolver
from general.utils import read_file


class RangeMap:
    def __init__(self,
                 destination_range_start: int,
                 source_range_start: int,
                 range_length: int,
                 ):
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    def try_get_destination(self, source: int):
        difference_with_source_start = source - self.source_range_start
        if 0 <= difference_with_source_start < self.range_length:
            return self.destination_range_start + difference_with_source_start
        else:
            return None

    def try_get_destination_range(self, source_range: 'Range') -> 'Range':
        if source_range.end < self.source_range_start \
                or source_range.start > self.source_range_start + self.range_length - 1:
            return None
        smallest_overlapping_source_number = max(self.source_range_start, source_range.start)
        greatest_overlapping_source_number = min(self.source_range_start + self.range_length - 1, source_range.end)
        return Range(
            start=self.try_get_destination(smallest_overlapping_source_number),
            end=self.try_get_destination(greatest_overlapping_source_number)
        )

    @staticmethod
    def from_line(line: str) -> 'RangeMap':
        dst, src, rng = line.split(" ")
        return RangeMap(
            destination_range_start=int(dst),
            source_range_start=int(src),
            range_length=int(rng),
        )

    def __str__(self):
        return f"(dest: {self.destination_range_start}, src: {self.source_range_start}, rng: {self.range_length})"


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def try_combine_with(self, other: 'Range') -> Optional['Range']:
        if self.start == other.start:
            return Range(self.start, max(self.end, other.end))
        if self.start < other.start and self.end >= other.end - 1:
            return Range(self.start, max(self.end, other.end))
        if self.start < other.start and self.end < other.end - 1:
            return None
        if self.start > other.start and other.end >= self.end - 1:
            return Range(other.start, max(self.end, other.end))
        if self.start > other.start and other.end < self.end - 1:
            return None

    def __str__(self):
        return f"Range({self.start}, {self.end})"


class SortedRangeCollection:
    def __init__(self):
        self.ranges: List[Range] = []

    def add_range(self, new_range: Range):
        if len(self.ranges) == 0:
            self.ranges.append(new_range)
            return

        i = 0
        old_range = self.ranges[i]
        while old_range.end < new_range.start:
            if i == len(self.ranges) - 1:
                self.ranges.append(new_range)
                return
            i += 1
            old_range = self.ranges[i]

        combined_range = old_range.try_combine_with(new_range)
        if combined_range is None:
            self.ranges.insert(i, new_range)
            return

        self.ranges[i] = combined_range
        if i + 1 >= len(self.ranges):
            return
        next_range = self.ranges[i + 1]
        next_combined_range = combined_range.try_combine_with(next_range)
        if combined_range is not None:
            self.ranges[i] = next_combined_range
            self.ranges.remove(next_range)


class SourceDestinationMapper:
    def __init__(self, range_maps: List[RangeMap]):
        self.range_maps: List[RangeMap] = range_maps

    def find_destination(self, source: int):
        for range_map in self.range_maps:
            destination = range_map.try_get_destination(source)
            if destination is not None:
                return destination
        return source

    def find_destination_ranges(self, source_ranges: SortedRangeCollection):
        combined_destination_ranges = SortedRangeCollection()
        for source_range in source_ranges.ranges:
            destination_ranges = [range_map.try_get_destination_range(source_range) for range_map in self.range_maps]
            destination_ranges = [item for item in destination_ranges if item is not None]
            for destination_range in destination_ranges:
                combined_destination_ranges.add_range(destination_range)
        return combined_destination_ranges

    @staticmethod
    def from_lines(lines: List[str]) -> 'SourceDestinationMapper':
        lines = lines[1:]
        return SourceDestinationMapper([RangeMap.from_line(line) for line in lines])


class ProblemSolverDay5(IProblemSolver):

    def solve_part_1(self):
        input_str = read_file(self.input_file_name)
        seeds_part, mappers_part = input_str.split("\n\n", 1)
        seeds = ProblemSolverDay5.get_seeds_part_1(seeds_part)
        sd_mappers = ProblemSolverDay5.get_source_destination_mappers(mappers_part)
        final_destinations: List[int] = [ProblemSolverDay5.find_location(seed, sd_mappers) for seed in seeds]
        return min(final_destinations)

    def solve_part_2(self):
        return
        input_str = read_file(self.input_file_name)
        seeds_part, mappers_part = input_str.split("\n\n", 1)
        seed_ranges = ProblemSolverDay5.get_seed_ranges(seeds_part)
        seed_range_collection = SortedRangeCollection()
        for seed_range in seed_ranges:
            seed_range_collection.add_range(seed_range)
        sd_mappers = ProblemSolverDay5.get_source_destination_mappers(mappers_part)
        final_destination_ranges = ProblemSolverDay5.find_location_ranges(seed_range_collection, sd_mappers)
        return final_destination_ranges.ranges[0].start

    @staticmethod
    def get_source_destination_mappers(mappers_part: str):
        sd_mappers: List[SourceDestinationMapper] = []
        mapper_strings = mappers_part.split("\n\n")
        for string in mapper_strings:
            sd_mappers.append(SourceDestinationMapper.from_lines(string.splitlines()))
        return sd_mappers

    @staticmethod
    def find_location(seed: int, sd_mappers: List[SourceDestinationMapper]):
        for mapper in sd_mappers:
            seed = mapper.find_destination(seed)
        return seed

    @staticmethod
    def get_seeds_part_1(seeds_str: str) -> List[int]:
        numbers_part = seeds_str.split(": ")[1]
        number_strings = numbers_part.split(" ")
        return [int(num) for num in number_strings]

    @staticmethod
    def get_seeds_part_2(seeds_str: str) -> List[int]:
        numbers = ProblemSolverDay5.get_seeds_part_1(seeds_str)
        seeds: List[int] = []
        for i in range(0, len(numbers), 2):
            start = numbers[i]
            length = numbers[i + 1]
            seeds.extend(range(start, start + length))
        return seeds

    @staticmethod
    def get_seed_ranges(seeds_str: str) -> List[Range]:
        numbers = ProblemSolverDay5.get_seeds_part_1(seeds_str)
        seed_ranges: List[Range] = []
        for i in range(0, len(numbers), 2):
            start = numbers[i]
            length = numbers[i + 1]
            seed_ranges.append(Range(start, start + length - 1))
        return seed_ranges

    @staticmethod
    def find_location_ranges(seed_range_collection: SortedRangeCollection, sd_mappers: List[SourceDestinationMapper]):
        source_ranges = seed_range_collection
        for mapper in sd_mappers:
            destination_range = mapper.find_destination_ranges(source_ranges)
            source_ranges = destination_range
        return source_ranges


if __name__ == '__main__':
    print(ProblemSolverDay5(use_smaller_input=True).solve())
    print(ProblemSolverDay5(use_smaller_input=False).solve())
