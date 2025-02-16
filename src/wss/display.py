class Step:
    nTubes: int
    from_tube: int
    to_tube: int

    def __init__(self, from_tube: int, to_tube: int, nTubes: int) -> None:
        self.from_tube = from_tube
        self.to_tube = to_tube
        self.nTubes = nTubes

    def __str__(self) -> str:
        state = ['% ' * self.nTubes]
        arrow = [' '] * self.nTubes * 2
        arrow[self.from_tube * 2] = '|'
        arrow[self.to_tube * 2] = '^'
        state.append(''.join(arrow))

        start, end = (
            max(self.from_tube, self.to_tube),
            min(self.from_tube, self.to_tube),
        )
        state.append(' ' * 2 * (start - 1) + '-' * 2 * (end - start + 1))

        return '\n'.join(state)

    def __repr__(self) -> str:
        return str(self)

    def __gt__(self, other: 'Step') -> bool:
        if self.from_tube == other.from_tube:
            return self.to_tube > other.to_tube
        return self.from_tube > other.from_tube

    def __lt__(self, other: 'Step') -> bool:
        if self.from_tube == other.from_tube:
            return self.to_tube < other.to_tube
        return self.from_tube < other.from_tube

    def __ge__(self, other: 'Step') -> bool:
        return self > other or self == other

    def __le__(self, other: 'Step') -> bool:
        return self < other or self == other
