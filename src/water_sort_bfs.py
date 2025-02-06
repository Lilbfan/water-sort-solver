import click
import json
import sys
from collections import deque
from copy import deepcopy
from typing import Optional

Tubes = list[list[str]]
Solution = list[list[list[str]]]


def parse_input(filename: str) -> Tubes:
    with open(filename, "r") as file:
        return json.load(file)["tubes"]


def is_solved(tubes: Tubes) -> bool:
    return all(len(set(tube)) <= 1 for tube in tubes)


def get_next_states(
    current_tubes: list[list[str]],
) -> list[tuple[int, int, list[list[str]]]]:
    next_states = []
    num_tubes = len(current_tubes)

    for i in range(num_tubes):
        if not current_tubes[i]:
            continue
        for j in range(num_tubes):
            if i == j:
                continue
            if (len(current_tubes[j]) == 0) or (
                len(current_tubes[j]) < 4
                and current_tubes[j][-1] == current_tubes[i][-1]
            ):
                new_tubes = deepcopy(current_tubes)
                color = new_tubes[i].pop()
                new_tubes[j].append(color)
                next_states.append((i, j, new_tubes))

    return next_states


def bfs_solve(start_tubes: Tubes) -> Optional[Solution]:
    queue = deque([(start_tubes, [])])
    visited = set()

    while queue:
        tubes, path = queue.popleft()
        state_key = tuple(tuple(tube) for tube in tubes)

        if state_key in visited:
            continue
        visited.add(state_key)

        if is_solved(tubes):
            return path

        for i, j, next_tubes in get_next_states(tubes):
            queue.append(
                (next_tubes, path + [[{"from": i, "to": j, "state": next_tubes}]])
            )

    print("No solution found", file=sys.stderr)
    exit(1)


@click.command()
@click.option("-f", "--filename", default="example_input.json", help="Input file")
def main(filename: str):
    tubes = parse_input(filename)
    solution = bfs_solve(tubes)
    print(json.dumps(solution))


if __name__ == "__main__":
    main()
