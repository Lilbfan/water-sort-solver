from was.water_sort_a_star import a_star_solve
from was.common import parse_input
import click


@click.command()
@click.option(
    "-f", "--filename", default="examples/example_input.json", help="Input file"
)
def main(filename: str):
    tubes = parse_input(filename)
    solution_a_star = a_star_solve(tubes)

    if solution_a_star is None:
        exit(1)

    for step in solution_a_star:
        print(step)


if __name__ == "__main__":
    main()
