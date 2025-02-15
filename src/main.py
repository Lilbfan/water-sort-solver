from wss.water_sort_a_star import a_star_solve
from wss.water_sort_bfs import bfs_solve
from wss.common import parse_input
import click
import tabulate


@click.command()
@click.option(
    "-f", "--filename", default="examples/example_input.json", help="Input file", type=str
)
@click.option(
    "-m", "--method", default="a_star",help="Solving method", type=click.Choice(['a_star', 'bfs'], case_sensitive=False)
)
def main(filename: str, method: str):
    tubes = parse_input(filename)
    if method == "bfs":
        solution = bfs_solve(tubes)
    else:
        solution = a_star_solve(tubes)

    if solution is None:
        exit(1)

    columns = ["No."] + [f"{i + 1}" for i in range(len(tubes))]
    table = []
    for idx, step in enumerate(solution):
        row = [idx + 1] + ["" for _ in range(step.nTubes)]
        start_tube = step.from_tube if step.from_tube < step.to_tube else step.to_tube
        end_tube = step.to_tube if step.from_tube < step.to_tube else step.from_tube
        for i in range(start_tube, end_tube + 1):
            row[i + 1] = ">" if step.from_tube < step.to_tube else "<"
        table.append(row)
    print(tabulate.tabulate(table, headers=columns, tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
