from sources.Grammars.Grammar import Grammar
from sources.Grammars.constant import EPS


class CockeYoungerKasami:
    def __init__(self, grammar: Grammar, convert_to_chomsky: bool = True):
        if convert_to_chomsky:
            grammar.convert_to_chomsky_normal_form()
        self.grammar = grammar

    def check_word_occurrence(self, word: str):
        if word == '':
            return (EPS,) in self.grammar.rules[self.grammar.start].rights

        check_dict: dict[str, dict[tuple[int, int], bool]] = dict()
        self.__init_check_dict_for_one_letters(word, check_dict)
        self.__init_all_check_dict(word, check_dict)

        if self.grammar.start not in check_dict:
            return False
        return check_dict[self.grammar.start][(0, len(word))]

    def __init_check_dict_for_one_letters(self, word: str,
                                          check_dict: dict[str, dict[tuple[int, int], bool]]):
        for ind, symbol in enumerate(word):
            for rule in self.grammar.rules.values():
                for transition in rule.rights:
                    if transition[0] in self.grammar.alphabet:
                        if symbol == transition[0]:
                            check_dict.setdefault(rule.left, dict())[(ind, ind + 1)] = True

    def __init_all_check_dict(self, word: str,
                              check_dict: dict[str, dict[tuple[int, int], bool]]):
        for length in range(2, len(word) + 1):
            for start_ind in range(len(word) - length + 1):
                end_ind = start_ind + length
                for rule in self.grammar.rules.values():
                    for transition in rule.rights:
                        if len(transition) == 2:
                            B = transition[0]
                            C = transition[1]
                            for middle in range(start_ind + 1, end_ind):
                                check_dict[rule.left][start_ind, end_ind] = \
                                    check_dict.setdefault(rule.left,
                                                          dict()).setdefault((start_ind,
                                                                              end_ind), False) or \
                                    check_dict.setdefault(B,
                                                          dict()).setdefault((start_ind,
                                                                              middle), False) and \
                                    check_dict.setdefault(C,
                                                          dict()).setdefault((middle,
                                                                              end_ind), False)
