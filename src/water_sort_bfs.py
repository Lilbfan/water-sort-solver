import click
import sys
from collections import deque
from copy import deepcopy
from typing import Optional
from display import Step
from common import parse_input, Tubes, MAX_TUBE_CAPACITY


def is_solved(tubes: Tubes) -> bool:
    return all(
        len(set(tube)) <= 1 and (len(tube) == 0 or len(tube) == MAX_TUBE_CAPACITY)
        for tube in tubes
    )


def num_able_to_move(tubes: Tubes, i: int, j: int) -> int:
    color = tubes[i].pop()
    n_move = 1
    while len(tubes[i]) > 0 and tubes[i][-1] == color:
        n_move += 1
        tubes[i].pop()

    if len(tubes[j]) == 0:
        return n_move

    if len(tubes[j]) + n_move <= MAX_TUBE_CAPACITY and tubes[j][-1] == color:
        return n_move
    return 0


def get_next_states(
    current_tubes: list[list[str]],
) -> list[tuple[int, int, Tubes]]:
    next_states = []
    num_tubes = len(current_tubes)

    for i in range(num_tubes):
        if not current_tubes[i]:
            continue
        for j in range(num_tubes):
            if i == j:
                continue
            n_move = num_able_to_move(deepcopy(current_tubes), i, j)
            if n_move != 0:
                new_tubes = deepcopy(current_tubes)
                for _ in range(n_move):
                    new_tubes[j].append(new_tubes[i].pop())
                next_states.append((i, j, new_tubes))

    return next_states


def bfs_solve(start_tubes: Tubes) -> Optional[list[Step]]:
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
                (next_tubes, path + [Step(from_tube=i, to_tube=j, nTubes=len(tubes))])
            )

    print("No solution found", file=sys.stderr)
    return None


@click.command()
@click.option("-f", "--filename", default="example_input.json", help="Input file")
def main(filename: str):
    tubes = parse_input(filename)
    solution = bfs_solve(tubes)
    if solution is None:
        exit(1)
    for step in solution:
        print(step)


if __name__ == "__main__":
    main()
