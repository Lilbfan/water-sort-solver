from water_sort_bfs import bfs_solve
from water_sort_a_star import a_star_solve
from common import parse_input
from display import Step
import click
import time


def diff(a: list[Step], b: list[Step]) -> bool:
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i].from_tube != b[i].from_tube or a[i].to_tube != b[i].to_tube:
            return False
    return True


@click.command()
@click.option("-f", "--filename", default="examples/example_input.json", help="Input file")
def main(filename: str):
    tubes = parse_input(filename)
    start_a_star = time.time()
    solution_a_star = a_star_solve(tubes)
    end_a_star = time.time()
    print("A* time:", end_a_star - start_a_star)

    start_bfs = time.time()
    solution_bfs = bfs_solve(tubes)
    end_bfs = time.time()
    print("BFS time:", end_bfs - start_bfs)

    if solution_a_star is None or solution_bfs is None:
        exit(1)

    if diff(solution_a_star, solution_bfs):
        print("Solutions are the same")
    else:
        print("Solutions are different")


if __name__ == "__main__":
    main()
