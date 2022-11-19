from sources.Grammars import Grammar
from sources.Grammars.constant import EPS
from sources.Grammars.rule import Rule
from itertools import chain
from copy import deepcopy


class DotNotation:
    def __init__(self, left: str, rule_ind: int, separate_ind: int, symbol: str, pose: int):
        self.left = left
        self.rule_ind = rule_ind
        self.separate_ind = separate_ind
        self.symbol = symbol
        self.pose = pose


class Earley:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.base_start = grammar.start
        grammar.add_new_start()
        self.new_start = grammar.start

    def check_word_occurrence(self, word: str):
        d_set = self.__make_d_sets(word)
        return d_set[-1][0]

    def __make_d_sets(self, word: str) -> list[list[list[DotNotation]]]:
        to_num = {symbol: i
                            for i, symbol in enumerate(chain(self.grammar.nonterminals, (EPS,),
                                                             self.grammar.alphabet))}
        d_sets: list[list[list[list[DotNotation]]]] = \
            [[[list()
               for left in range(len(self.grammar.nonterminals))]
              for right_first in range(len(to_num) + 1)]
             for j in range(len(word) + 1)]
        d_sets[0][
            to_num[self.base_start]][
            to_num[self.new_start]].append(DotNotation(self.new_start,
                                                                 0,
                                                                 0,
                                                                 self.base_start,
                                                                 0))
        for length in range(len(word) + 1):
            self.__scan(word, d_sets, length, to_num)
            copy_d_sets = deepcopy(d_sets)
            # queue = d_sets[ind]
            # while copy_d_sets != d_sets:
            #     changes |= self.__predict(d_sets, length, to_num)
            #     changes |= self.__complete(d_sets, length, to_num)
        return d_sets[len(word)]

    def __scan(self, word: str, d_sets: list[list[list[list[DotNotation]]]], ind: int,
               to_num: dict[str, int]):
        if ind == 0:
            return
        for nonterm_sets in d_sets[ind - 1][to_num[word[ind - 1]]]:
            for situation in nonterm_sets:
                transition = self.grammar.rules[situation.left].rights[situation.rule_ind]
                new_separate_ind = situation.separate_ind + 1
                right_first = transition[situation.separate_ind]
                d_sets[ind][to_num[right_first]][to_num[situation.left]].append(
                    DotNotation(situation.left,
                                situation.rule_ind,
                                new_separate_ind,
                                right_first,
                                situation.pose))

    def __predict(self, d_sets: list[list[list[list[DotNotation]]]],
                  ind: int,
                  to_num: dict[str, int]):
        changes = False
        copy_d_sets = deepcopy(d_sets)
        for right_first_sets in copy_d_sets[ind][:len(self.grammar.nonterminals)]:
            for from_letter_sets in right_first_sets:
                for situation in from_letter_sets:
                    right_first = situation.symbol
                    for rule_ind, transition in enumerate(self.grammar.rules[right_first].rights):
                        changes = True
                        d_sets[ind][to_num[transition[0]]][to_num[right_first]].append(
                            DotNotation(right_first, rule_ind, 0, transition[0], ind)
                        )
        return changes

    def __complete(self, d_sets: list[list[list[list[DotNotation]]]], ind: int,
                   to_num: dict[str, int]):
        changes = False
        copy_d_sets = deepcopy(d_sets)
        for first_letter_sets in copy_d_sets[ind][:len(self.grammar.nonterminals) + 1]:
            for from_letter_sets in first_letter_sets:
                for situation in from_letter_sets:
                    left = situation.left
                    rule_ind = situation.rule_ind
                    pose = situation.pose
                    if situation.separate_ind == len(self.grammar.rules[left].rights[rule_ind]) or \
                            self.grammar.rules[left].rights[rule_ind] == (EPS,):
                        for up_letter_from_sets in copy_d_sets[pose][to_num[left]]:
                            for up_situation in up_letter_from_sets:
                                changes = True
                                up_left = up_situation.left
                                up_rule_ind = up_situation.rule_ind
                                up_separate = up_situation.separate_ind
                                up_transition = self.grammar.rules[up_left].rights[up_rule_ind]
                                if up_separate < len(up_transition) - 1:
                                    up_first_letter = up_transition[up_separate]
                                else:
                                    up_first_letter = EPS
                                up_separate += 1
                                d_sets[ind][
                                    to_num[up_first_letter]][
                                    to_num[up_left]].append(
                                    DotNotation(up_left,
                                                up_rule_ind,
                                                up_situation.separate_ind+1,
                                                up_first_letter,
                                                up_situation.pose))
        return changes
