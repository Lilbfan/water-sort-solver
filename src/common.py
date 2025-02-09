import json

Tubes = list[list[str]]
MAX_TUBE_CAPACITY = 4


def parse_input(filename: str) -> Tubes:
    with open(filename, "r") as file:
        return json.load(file)["tubes"]
