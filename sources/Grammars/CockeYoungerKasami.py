from sources.Grammars.Grammar import Grammar
from sources.Grammars.constant import EPS


class CockeYoungerKasami:
    """Cocke-Younger-Kasami algorithm,
    Usage: create an object for some grammar,
    with check_word_occurrence method check
    if given word belongs to grammar language"""
    def __init__(self, grammar: Grammar, convert_to_chomsky: bool = True):
        """Build CYK object, optional convert to Chomsky normal form"""
        if convert_to_chomsky:
            grammar.convert_to_chomsky_normal_form()
        self.grammar = grammar

    def check_word_occurrence(self, word: str):
        """Return True if word belongs to grammar language"""
        if word == '':
            return (EPS,) in self.grammar.rules[self.grammar.start].rights

        check_list: list[list[list[bool]]] = [[[False for i in range(len(word) + 1)]
                                               for j in range(len(word))]
                                              for k in range(len(self.grammar.rules))]
        number_of_nonterm = {nonterm: i for i, nonterm in enumerate(self.grammar.rules.keys())}
        self.__init_check_dict_for_one_letters(word, check_list, number_of_nonterm)
        self.__init_all_check_dict(word, check_list, number_of_nonterm)

        return check_list[number_of_nonterm[self.grammar.start]][0][len(word)]

    def __init_check_dict_for_one_letters(self, word: str,
                                          check_list: list[list[list[bool]]],
                                          ind_nonterm: dict[str, int]):
        for ind, symbol in enumerate(word):
            for rule in self.grammar.rules.values():
                for transition in rule.rights:
                    if transition[0] in self.grammar.alphabet:
                        if symbol == transition[0]:
                            check_list[ind_nonterm[rule.left]][ind][ind + 1] = True

    def __init_all_check_dict(self, word: str,
                              check_list: list[list[list[bool]]],
                              ind: dict[str, int]):
        for length in range(2, len(word) + 1):
            for start_ind in range(len(word) - length + 1):
                end_ind = start_ind + length
                for rule in self.grammar.rules.values():
                    for transition in rule.rights:
                        if len(transition) == 2:
                            left = transition[0]
                            right = transition[1]
                            for middle in range(start_ind + 1, end_ind):
                                check_list[ind[rule.left]][start_ind][end_ind] |= \
                                    check_list[ind[left]][start_ind][middle] and \
                                    check_list[ind[right]][middle][end_ind]
