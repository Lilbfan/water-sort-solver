import click
import sys
from heapq import heappop, heappush
from typing import Optional
from display import Step
from common import parse_input, Tubes, MAX_TUBE_CAPACITY


def is_solved(tubes: Tubes) -> bool:
    return all(
        len(set(tube)) <= 1 and (len(tube) == 0 or len(tube) == MAX_TUBE_CAPACITY)
        for tube in tubes
    )


def num_able_to_move(tubes: Tubes, i: int, j: int) -> int:
    if not tubes[i] or (
        tubes[j]
        and (len(tubes[j]) == MAX_TUBE_CAPACITY or tubes[j][-1] != tubes[i][-1])
    ):
        return 0
    color = tubes[i][-1]
    n_move = 1
    while n_move < len(tubes[i]) and tubes[i][-1 - n_move] == color:
        n_move += 1
    return (
        n_move
        if len(tubes[j]) == 0 or (len(tubes[j]) + n_move <= MAX_TUBE_CAPACITY)
        else 0
    )


def get_next_states(current_tubes: Tubes) -> list[tuple[int, int, Tubes]]:
    next_states = []
    num_tubes = len(current_tubes)

    for i in range(num_tubes):
        if not current_tubes[i]:
            continue
        for j in range(num_tubes):
            if i == j or len(current_tubes[j]) == MAX_TUBE_CAPACITY:
                continue
            n_move = num_able_to_move(current_tubes, i, j)
            if n_move > 0:
                new_tubes = [tube[:] for tube in current_tubes]  # Shallow copy
                for _ in range(n_move):
                    new_tubes[j].append(new_tubes[i].pop())
                next_states.append((i, j, new_tubes))

    return next_states


def heuristic(tubes: Tubes) -> int:
    return sum(len(set(tube)) - 1 for tube in tubes if tube)


def a_star_solve(start_tubes: Tubes) -> Optional[list[Step]]:
    queue = [(heuristic(start_tubes), 0, start_tubes, [])]
    visited = set()

    def state_key(tubes: Tubes):
        return frozenset((i, tuple(tubes[i])) for i in range(len(tubes)))

    while queue:
        _, cost, tubes, path = heappop(queue)
        key = state_key(tubes)

        if key in visited:
            continue
        visited.add(key)

        if is_solved(tubes):
            return path

        for i, j, next_tubes in get_next_states(tubes):
            heappush(
                queue,
                (
                    cost + heuristic(next_tubes),
                    cost + 1,
                    next_tubes,
                    path + [Step(from_tube=i, to_tube=j, nTubes=len(tubes))],
                ),
            )

    print("No solution found", file=sys.stderr)
    return None


@click.command()
@click.option("-f", "--filename", default="example_input.json", help="Input file")
def main(filename: str):
    tubes = parse_input(filename)
    solution = a_star_solve(tubes)
    if solution is None:
        exit(1)
    for step in solution:
        print(step)


if __name__ == "__main__":
    main()
