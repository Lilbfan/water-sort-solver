from wss.water_sort_bfs import bfs_solve
from wss.water_sort_a_star import a_star_solve
from wss.common import parse_input
from wss.display import Step
import click
import datetime
import time
import tabulate


def diff(a: list[Step], b: list[Step]) -> bool:
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i].from_tube != b[i].from_tube or a[i].to_tube != b[i].to_tube:
            return False
    return True


@click.command()
@click.option(
    "-f", "--filename", default="examples/example_input.json", help="Input file"
)
def main(filename: str):
    tubes = parse_input(filename)
    start_a_star = time.time()
    solution_a_star = a_star_solve(tubes)
    print("A* time:", datetime.timedelta(seconds=time.time() - start_a_star))

    start_bfs = time.time()
    solution_bfs = bfs_solve(tubes)
    print("BFS time:", datetime.timedelta(seconds=time.time() - start_bfs))

    if solution_a_star is None or solution_bfs is None:
        exit(1)

    if diff(solution_a_star, solution_bfs):
        print("\033[92mSolutions are the same\033[0m")
    else:
        print("\033[91mSolutions are different\033[0m")
        columns = ["step", "A*", "BFS"]
        table = []
        for i in range(max(len(solution_a_star), len(solution_bfs))):
            solution_a_star_step = (
                f"{solution_a_star[i].from_tube}->{solution_a_star[i].to_tube}"
                if i < len(solution_a_star)
                else ""
            )
            solution_bfs_step = (
                f"{solution_bfs[i].from_tube}->{solution_bfs[i].to_tube}"
                if i < len(solution_bfs)
                else ""
            )
            table.append([i, solution_a_star_step, solution_bfs_step])
        print(tabulate.tabulate(table, headers=columns, tablefmt="rounded_grid"))


if __name__ == "__main__":
    main()
