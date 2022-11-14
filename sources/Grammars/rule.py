from sources.Grammars.constant import EPS


class Rule:
    def __init__(self, left: str, *rights: tuple[str]):
        self.left: str = left
        self.rights: list[tuple[str]] = list(rights)

    def add(self, right: tuple = tuple()):
        if not right:
            right = (EPS,)
        self.rights.append(right)

    def __str__(self):
        return f"{self.left} -> {'|'.join(list(map(''.join, self.rights)))}"
