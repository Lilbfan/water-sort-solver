from was.water_sort_a_star import a_star_solve
from was.common import parse_input
import click


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

    for step in solution:
        print(step)


if __name__ == "__main__":
    main()
