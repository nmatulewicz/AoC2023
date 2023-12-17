import queue
from typing import List, Literal, Dict, get_args, Tuple

import attr

from general.problem_solver_interface import IProblemSolver
from general.utils import lines_to_int_array

Direction = Literal["N", "E", "S", "W"]


def are_opposites(d1: Direction, d2: Direction):
    match d1:
        case "N":
            return d2 == "S"
        case "S":
            return d2 == "N"
        case "E":
            return d2 == "W"
        case "W":
            return d2 == "E"


def get_coordinates(row, col, direction: Direction):
    match direction:
        case "N":
            return row - 1, col
        case "S":
            return row + 1, col
        case "E":
            return row, col + 1
        case "W":
            return row, col - 1


@attr.dataclass
class Node:
    row: int
    column: int
    last_taken_direction: Direction
    repetitively_taken_direction: int


def node_to_tuple(node):
    return node.row, node.column, node.last_taken_direction, node.repetitively_taken_direction


def node_from_tuple(tup):
    row, column, last_taken_direction, repetitively_taken_direction = tup
    return Node(
        row=row,
        column=column,
        last_taken_direction=last_taken_direction,
        repetitively_taken_direction=repetitively_taken_direction
    )


@attr.dataclass
class DijkstraInfo:
    previous_node: Node
    shortest_path: int


class ProblemSolver(IProblemSolver):

    def solve_part_1(self):
        input_array = lines_to_int_array(self.lines)
        destination_row, destination_col = input_array.shape
        destination_col -= 1
        destination_row -= 1

        visited_nodes: Dict[Tuple[int, int, Direction, int], DijkstraInfo] = {}
        found_paths: queue.PriorityQueue = queue.PriorityQueue()

        # add start node
        for i in range(1, 4):
            for direction in get_args(Direction):
                start_node = Node(row=0, column=0, last_taken_direction=direction, repetitively_taken_direction=0)
        start_node = Node(row=0, column=0, last_taken_direction="E", repetitively_taken_direction=0)
        found_paths.put((0, start_node))

        # repeat until destination is reached
        current_dist, current_node = found_paths.get()  # type: int, Node
        while not (current_node.row == destination_row and current_node.column == destination_col):
            for direction in get_args(Direction):
                if are_opposites(current_node.last_taken_direction, direction):
                    continue
                row, col = get_coordinates(current_node.row, current_node.column, direction)
                if not (0 <= row <= destination_row and 0 <= col <= destination_col):
                    continue
                if current_node.last_taken_direction == direction:
                    repetitively_taken_direction = current_node.repetitively_taken_direction + 1
                    if repetitively_taken_direction > 3:
                        continue
                else:
                    repetitively_taken_direction = 1
                next_node = Node(
                    row=row,
                    column=col,
                    last_taken_direction=direction,
                    repetitively_taken_direction=repetitively_taken_direction
                )
                # if next_node in visited_nodes:
                if visited_nodes.get(node_to_tuple(next_node), None) is not None:
                    continue
                next_distance = current_dist + input_array[row, col]
                dijkstra_info = DijkstraInfo(previous_node=current_node, shortest_path=next_distance)

                visited_nodes[node_to_tuple(next_node)] = dijkstra_info
                found_paths.put((next_distance, next_node))

                while repetitively_taken_direction < 3:
                    repetitively_taken_direction += 1
                    next_node = Node(
                        row=row,
                        column=col,
                        last_taken_direction=direction,
                        repetitively_taken_direction=repetitively_taken_direction
                    )
                    visited_nodes[node_to_tuple(next_node)] = dijkstra_info
            current_dist, current_node = found_paths.get()

        return current_dist

    def solve_part_2(self):
        pass


if __name__ == '__main__':
    print(ProblemSolver(use_smaller_input=True).solve())
    print(ProblemSolver(use_smaller_input=False).solve())
