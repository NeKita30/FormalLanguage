from sources.Grammars.constant import EPS


class Rule:
    """Rule class with __str__ method to represent grammar,
    has left nonterminal and list of transitions"""
    def __init__(self, left: str, *rights: tuple[str]):
        self.left: str = left
        self.rights: list[tuple[str]] = list(rights)

    def add(self, right: tuple = tuple()):
        """Adding new transition to rule"""
        if not right:
            right = (EPS,)
        if right not in self.rights:
            self.rights.append(right)

    def __str__(self):
        return f"{self.left} -> {'|'.join(list(map(''.join, self.rights)))}"
