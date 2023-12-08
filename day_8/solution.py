import math
from enum import StrEnum
from typing import List, Dict, Callable

import attr

from general.problem_solver_interface import IProblemSolver

@attr.dataclass
class Node:
    name: str
    left: str
    right: str


@attr.dataclass
class Graph(Dict[str, Node]):
    pass


class Direction(StrEnum):
    Left = "L"
    Right = "R"


@attr.dataclass
class DirectionIterator:
    _left_right_instructions: str
    _current_index: int = 0

    def next(self) -> Direction:
        next_direction = Direction(self._left_right_instructions[self._current_index])
        self._current_index += 1
        if self._current_index == len(self._left_right_instructions):
            self._current_index = 0
        return next_direction


def process_input(lines: List[str]):
    left_right_instructions = lines[0]
    direction_iterator = DirectionIterator(left_right_instructions)
    graph = Graph()
    for line in lines[2:]:
        node_name, left_right_part = line.split(" = ")  # type: str
        left, right = left_right_part.strip("()").split(", ")
        graph[node_name] = Node(name=node_name, left=left, right=right)
    return direction_iterator, graph


def is_zzz(string: str):
    x = string == "ZZZ"
    return string == "ZZZ"


def ends_with_z(string: str):
    x = string.endswith("Z")
    return string.endswith("Z")


class ProblemSolver(IProblemSolver):
    def solve_part_1(self, start_node_name="AAA", is_destination_func: Callable[[str], bool] = is_zzz):
        direction_iterator, graph = process_input(self.lines)
        current_node = graph.get(start_node_name)
        next_direction = direction_iterator.next()
        steps = 0
        while not is_destination_func(current_node.name):
            if next_direction == Direction.Left:
                next_node = graph.get(current_node.left)
            else:
                next_node = graph.get(current_node.right)
            current_node = next_node
            steps += 1
            next_direction = direction_iterator.next()
        return steps

    def solve_part_2(self):
        direction_iterator, graph = process_input(self.lines)
        start_nodes = [node for node in graph.values() if node.name.endswith("A")]
        required_steps = [self.solve_part_1(start_node_name=node.name, is_destination_func=ends_with_z)
                          for node in start_nodes]
        return math.lcm(*required_steps)


if __name__ == '__main__':
    print(ProblemSolver(use_smaller_input=True).solve())
    print(ProblemSolver(use_smaller_input=False).solve())
