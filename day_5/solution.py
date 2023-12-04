from typing import List

from general.problem_solver_interface import IProblemSolver


class ProblemSolverDay5(IProblemSolver):

    def solve_part_1(self, lines: List[str]):
        pass

    def solve_part_2(self, lines: List[str]):
        pass


if __name__ == '__main__':
    print(ProblemSolverDay5(use_smaller_input=True).solve())
    print(ProblemSolverDay5(use_smaller_input=False).solve())