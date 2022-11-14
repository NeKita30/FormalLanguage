class TranslateGrammarError(Exception):
    def __init__(self, code="", *args):
        self.code = code
        self.args = args

    def __str__(self):
        if self.code == "extension":
            return f"Wrong \"{self.args[0]}\" file name - should end with .grm"

        if self.code == "non-term":
            return f"""Wrong nonterminal list line - should be:
Nonterm.: A B A_1 C D\\B
but get:
{self.args[0]}"""

        if self.code == "non-term":
            return f"""Wrong alphabet line - should be:
Alphabet: a b c a_1 a_2 
but get:
{self.args[0]}"""

        if self.code == "alpha_non-term":
            return f"""Wrong nonterminal set and alphabet - should be disjoint,
but get: {self.args[0]}"""

        if self.code == "start":
            return f"""Wrong start nonterminal line - should be:
Start: S
but get:
{self.args[0]}"""

        if self.code == "unknown-non-term":
            return f"""Unknown nonterminal - \"{self.args[0]}\" not in nonterminal set: {self.args[1]}"""

        if self.code == "unknown-symbol":
            return f"""Unknown symbol - \"{self.args[0]}\" - in transition {self.args[1]}"""

        if self.code == "rule":
            return f"""Wrong rule line: {self.args[0]}
Must be:
A -> a  or
A -> A...B  or
A -> AaBbcD  or
A -> Ab | Bd | A_1A_2 | ε"""


class ConvertingGrammarError(Exception):
    def __init__(self, code="", *args):
        self.code = code
        self.args = args

    def __str__(self):
        pass
