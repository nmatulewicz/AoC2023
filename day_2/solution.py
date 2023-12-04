from typing import List, Tuple

from general.problem_solver_interface import IProblemSolver


class CubeSet:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def can_be_drawn_from(self, other: 'CubeSet'):
        return self.red <= other.red \
            and self.green <= other.green \
            and self.blue <= other.blue

    @staticmethod
    def from_line_part(line_part: str):
        draw = CubeSet()
        string_parts = line_part.split(",")
        for part in string_parts:
            part = part.removeprefix(" ")
            number_string, color_string = part.split(" ")
            number = int(number_string)
            setattr(draw, color_string, number)
        return draw

    def __str__(self):
        return f"{{r: {self.red}, g: {self.green}, b: {self.blue}}}"


class Game:
    def __init__(self, id: int, draws: List[CubeSet]):
        self.id = id
        self.draws = draws

    def is_possible(self, bag_contents: CubeSet):
        return all(draw.can_be_drawn_from(bag_contents) for draw in self.draws)

    def compute_power(self):
        min_red = max([draw.red for draw in self.draws])
        min_green = max([draw.green for draw in self.draws])
        min_blue = max([draw.blue for draw in self.draws])
        return min_red * min_blue * min_green

    @staticmethod
    def from_line(line: str):
        id_part, sets_line_part = line.split(":")  # type: str
        id = int(id_part.split(" ")[1])
        set_line_parts = sets_line_part.split(";")
        return Game(id=id, draws=[CubeSet.from_line_part(part) for part in set_line_parts])


class ProblemSolverDay2(IProblemSolver):

    def solve_part_1(self, lines: List[str]):
        bag_contents = CubeSet(red=12, green=13, blue=14)
        games = [Game.from_line(line) for line in lines]
        valid_game_ids = [game.id for game in games if game.is_possible(bag_contents)]
        return sum(valid_game_ids)

    def solve_part_2(self, lines: List[str]):
        games = [Game.from_line(line) for line in lines]
        powers = [game.compute_power() for game in games]
        return sum(powers)


if __name__ == '__main__':
    print(ProblemSolverDay2(use_smaller_input=True).solve())
    print(ProblemSolverDay2(use_smaller_input=False).solve())
