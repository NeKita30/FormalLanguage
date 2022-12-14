from sources.Grammars import Grammar
from sources.Grammars.constant import EPS
from collections import defaultdict


class DotNotation:
    """Dot notation, in russian called situation;
    needs rule, index of dot and position"""
    def __init__(self, left: str, rule: tuple[str],
                 separate_ind: int, symbol: str, pose: int):
        self.left = left
        self.rule: tuple[str] = rule
        self.separate_ind = separate_ind
        self.symbol = symbol
        self.pose = pose


class Earley:
    """Earley algorithm;
    Usage: create an object for some grammar,
    with check_word_occurrence method check
    if given word belongs to grammar language"""
    def __init__(self, grammar: Grammar, add_new_start=True):
        """Build Earley object, optional add new start nonterminal to grammar"""
        self.grammar = grammar
        if add_new_start:
            grammar.add_new_start()
        self.new_start = grammar.start
        self.base_start = grammar.rules[self.new_start].rights[0][0]
        self.lst_symbols = grammar.nonterminals + [EPS] + grammar.alphabet
        self.to_num = {symbol: i for i, symbol in enumerate(self.lst_symbols)}

    def check_word_occurrence(self, word: str):
        """Return True if word belongs to grammar language"""
        state_set_flags = self.__make_d_sets(word)
        return state_set_flags[self.to_num[self.new_start], (self.base_start,), 1, 0]

    def __make_d_sets(self, word: str) -> dict[tuple[int, tuple[str], int, int], bool]:
        state_sets: list[list[list[DotNotation]]] = [[list()
                                                      for _ in self.lst_symbols]
                                                     for _ in range(len(word) + 1)]
        state_sets[0][self.to_num[self.base_start]] = [
            DotNotation(self.new_start,
                        self.grammar.rules[self.new_start].rights[0],
                        0,
                        self.base_start,
                        0)]
        state_set_flags: list[dict[tuple[int, tuple[str], int, int], bool]] = \
            [defaultdict(bool) for _ in range(len(word) + 1)]

        for length in range(len(word) + 1):
            queue = self.__make_queue(state_sets[length])
            while queue:
                situation = queue.pop(0)
                self.__predict(situation, state_sets, length, queue, state_set_flags)
                self.__complete(situation, state_sets, length, queue, state_set_flags)
            self.__scan(word, state_sets, length, state_set_flags)
        return state_set_flags[len(word)]

    @staticmethod
    def __make_queue(d_set: list[list[DotNotation]]):
        queue = list()
        for lst in d_set:
            for situation in lst:
                queue.append(situation)
        return queue

    def __scan(self, word: str, state_sets: list[list[list[DotNotation]]], ind: int,
               state_set_flags: list[dict[tuple[int, tuple[str], int, int], bool]]):
        if ind == len(word):
            return
        if not word[ind] in self.grammar.alphabet:
            return
        for situation in state_sets[ind][self.to_num[word[ind]]]:
            if not state_set_flags[ind + 1][self.to_num[situation.left],
                                            situation.rule,
                                            situation.separate_ind + 1,
                                            situation.pose]:
                transition = situation.rule
                new_separate_ind = situation.separate_ind + 1
                new_right_first = (transition + (EPS,))[new_separate_ind]
                state_set_flags[ind + 1][self.to_num[situation.left],
                                         situation.rule,
                                         situation.separate_ind + 1,
                                         situation.pose] = True
                state_sets[ind + 1][self.to_num[new_right_first]].append(
                    DotNotation(situation.left,
                                situation.rule,
                                new_separate_ind,
                                new_right_first,
                                situation.pose))

    def __predict(self, situation: DotNotation, state_sets: list[list[list[DotNotation]]],
                  ind: int, queue: list[DotNotation],
                  state_set_flags: list[dict[tuple[int, tuple[str], int, int], bool]]):
        if situation.symbol in self.grammar.nonterminals:
            for transition in self.grammar.rules[situation.symbol].rights:
                if not state_set_flags[ind][self.to_num[situation.symbol],
                                            transition, 0, ind]:
                    next_symbol = transition[0]
                    state_sets[ind][self.to_num[next_symbol]].append(
                        DotNotation(situation.symbol, transition, 0, next_symbol, ind)
                    )
                    state_set_flags[ind][self.to_num[situation.symbol],
                                         transition, 0, ind] = True
                    queue.append(state_sets[ind][self.to_num[next_symbol]][-1])

    def __complete(self, situation: DotNotation, state_sets: list[list[list[DotNotation]]],
                   ind: int, queue: list[DotNotation],
                   state_set_flags: list[dict[tuple[int, tuple[str], int, int], bool]]):
        left, right, pose = situation.left, situation.rule, situation.pose
        if situation.separate_ind == len(right) or right == (EPS,):
            for up_situation in state_sets[pose][self.to_num[left]]:
                if not state_set_flags[ind][self.to_num[up_situation.left],
                                            up_situation.rule,
                                            up_situation.separate_ind + 1,
                                            up_situation.pose]:
                    state_set_flags[ind][self.to_num[up_situation.left],
                                         up_situation.rule,
                                         up_situation.separate_ind + 1,
                                         up_situation.pose] = True
                    up_left = up_situation.left
                    up_rule = up_situation.rule
                    up_pose = up_situation.pose
                    up_separate_ind = up_situation.separate_ind + 1
                    up_next_symbol = (up_rule + (EPS,))[up_separate_ind]
                    state_sets[ind][self.to_num[up_next_symbol]].append(
                        DotNotation(up_left, up_rule, up_separate_ind,
                                    up_next_symbol, up_pose)
                    )
                    queue.append(state_sets[ind][self.to_num[up_next_symbol]][-1])
