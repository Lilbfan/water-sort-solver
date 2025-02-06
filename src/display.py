class Step:
    nTubes: int
    from_tube: int
    to_tube: int

    def __init__(self, from_tube: int, to_tube: int, nTubes: int) -> None:
        self.from_tube = from_tube
        self.to_tube = to_tube
        self.nTubes = nTubes

    def __str__(self) -> str:
        state = ["% " * self.nTubes]

        arrow = [" "] * self.nTubes * 2
        arrow[self.from_tube * 2] = "|"
        arrow[self.to_tube * 2] = "^"
        state.append("".join(arrow))

        start, end = (
            max(self.from_tube, self.to_tube),
            min(self.from_tube, self.to_tube),
        )
        state.append(" " * 2 * (start - 1) + "-" * 2 * (end - start + 1))

        return "\n".join(state) + "\n\n\n"

    def __repr__(self) -> str:
        return str(self)
