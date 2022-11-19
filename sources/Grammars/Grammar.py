from sources.Grammars.constant import EPS
from sources.parse_and_translate import translaters_grammar
from sources.Grammars.rule import Rule
import copy
import random
import sources.Grammars.errors as err


class Grammar:
    def __init__(self, grm_file: str):
        self.rules: dict[str, Rule] = dict()
        self.alphabet: list[str] = list()
        self.nonterminals: list[str] = list()
        self.start = ""
        translaters_grammar.translate_from_grm(grm_file, self)

    def write_as_grm(self, grm_file: str):
        translaters_grammar.translate_to_grm(grm_file, self)

    def convert_to_chomsky_normal_form(self, study_mode: str = ""):
        converting_to_chomsky_process = [self.__delete_no_generating_nonterminals,
                                         self.__delete_unreachable_nonterminals,
                                         self.__delete_mixed_transitions,
                                         self.__delete_long_transitions,
                                         self.__delete_eps_transitions,
                                         self.__delete_unit_transitions]
        for step, function in enumerate(converting_to_chomsky_process):
            function()
            if study_mode:
                self.write_as_grm(f"{study_mode}_step_{step + 1}.grm")

    def generate_word(self, limit=-1):
        word = [self.start]
        while True:
            changes = False
            new_word = list()
            for symbol in word:
                new_symbols = (symbol,)
                if symbol in self.nonterminals:
                    changes |= True
                    if limit == 0 and (EPS,) in self.rules[symbol].rights:
                        new_symbols = (EPS,)
                    else:
                        new_symbols = random.choice(self.rules[symbol].rights)
                        if new_symbols != (EPS,):
                            limit = 0 if limit == 0 else limit - 1
                new_word += new_symbols
            word = new_word
            if not changes:
                break
        word = "".join(word).replace(EPS, "")
        return word

    def check_chomsky_form(self):
        for left, rule in self.rules.items():
            for transition in rule.rights:
                if len(transition) == 1:
                    if transition[0] not in self.alphabet:
                        if left != self.start or transition[0] != (EPS,):
                            return False
                elif len(transition) == 2:
                    if transition[0] not in self.nonterminals \
                            or transition[1] not in self.nonterminals \
                            or transition[0] == self.start \
                            or transition[1] == self.start:
                        return False
                else:
                    return False
        return True

    def add_new_start(self):
        self.__add_new_start(False)

    def __delete_no_generating_nonterminals(self):
        lst_no_generating_nonterminals = self.__mark_non_generating_nonterminals()
        for nonterminal in self.nonterminals:
            if nonterminal in lst_no_generating_nonterminals:
                if nonterminal in self.rules:
                    self.rules.pop(nonterminal)
                continue
            lst_no_generating_transitions_ind = list()
            for ind_trans, transition in enumerate(self.rules[nonterminal].rights):
                generating_transition = True
                for symbol in transition:
                    generating_transition &= symbol == EPS or symbol in self.alphabet \
                                             or symbol not in lst_no_generating_nonterminals
                if not generating_transition:
                    lst_no_generating_transitions_ind.append(ind_trans)
            for ind_trans in lst_no_generating_transitions_ind:
                self.rules[nonterminal].rights.pop(ind_trans)
        self.nonterminals = list(self.rules.keys())

    def __delete_unreachable_nonterminals(self):
        if self.start not in self.nonterminals:
            self.nonterminals.clear()
            self.rules.clear()
            return
        reached = [self.start]
        queue = [self.start]
        while queue:
            nonterminal = queue.pop(0)
            for transition in self.rules[nonterminal].rights:
                for symbol in transition:
                    if symbol in self.nonterminals and symbol not in reached:
                        reached.append(symbol)
                        queue.append(symbol)
        for nonterminal in self.nonterminals:
            if nonterminal not in reached:
                if nonterminal in self.rules:
                    self.rules.pop(nonterminal)
        self.nonterminals = reached

    def __delete_mixed_transitions(self):
        new_rules = dict()
        terminal_replace = dict()
        for left, rule in self.rules.items():
            unmixed_rule = Rule(left)
            for transition in rule.rights:
                new_transition = transition
                if len(transition) > 1:
                    new_transition = list()
                    for symbol in transition:
                        new_symbol = symbol
                        if symbol in self.alphabet:
                            new_symbol = \
                                terminal_replace.setdefault(symbol,
                                                            Grammar.__search_new_nonterminal(
                                                                self.nonterminals + self.alphabet,
                                                                end="_" + symbol))
                            if new_symbol not in self.nonterminals:
                                new_rules[new_symbol] = Rule(new_symbol, (symbol,))
                                self.nonterminals.append(new_symbol)
                        new_transition.append(new_symbol)
                unmixed_rule.add(tuple(new_transition))
            new_rules[left] = unmixed_rule
        self.rules = new_rules

    def __delete_long_transitions(self):
        new_rules = dict()
        number = 0
        long_transition_replace = dict()
        for left, rule in self.rules.items():
            new_rules[left] = Rule(left)
            for transition in rule.rights:
                new_left = left
                new_right = [transition[0]]
                for ind, next_symbol in enumerate(transition[1:]):
                    if ind == len(transition) - 2:
                        new_right.append(next_symbol)
                        continue
                    if transition[ind + 1:] in long_transition_replace:
                        new_nonterminal = long_transition_replace[transition[ind + 1:]]
                    else:
                        new_nonterminal = Grammar.__search_new_nonterminal(
                            self.nonterminals + self.alphabet, end="_" + str(number := number + 1))
                        long_transition_replace[transition[ind + 1:]] = new_nonterminal
                    self.nonterminals.append(new_nonterminal)
                    new_right.append(new_nonterminal)
                    new_rules[new_left].add(tuple(new_right))
                    new_left = new_nonterminal
                    new_right = [next_symbol]
                    new_rules[new_left] = Rule(new_left)
                new_rules[new_left].add(tuple(new_right))
        self.rules = new_rules

    def __delete_eps_transitions(self):
        eps_transitions = list()
        new_nonterminal = self.nonterminals.copy()
        new_rules = copy.deepcopy(self.rules)
        dependences = self.__make_dependences_dict()
        self.__mark_eps_transitions(eps_transitions)
        eps_generating = eps_transitions.copy()
        transition_eps_count = dict()
        queue = eps_generating.copy()
        while queue:
            non_term = queue.pop(0)
            for dependent in dependences.get(non_term, list()):
                if dependent not in eps_generating:
                    for transition in self.rules[dependent].rights:
                        if non_term in transition:
                            transition_eps_count[(dependent, transition)] = \
                                transition_eps_count.setdefault((dependent, transition), 0) + 1
                            if transition_eps_count[(dependent, transition)] == len(transition):
                                eps_generating.append(dependent)
                                queue.append(dependent)

        self.__adding_new_rules_for_eps_generating(new_rules, eps_generating)
        empty_word_in_language = (EPS,) in self.rules[self.start].rights
        self.rules = new_rules
        self.nonterminals = new_nonterminal
        self.__deleting_eps(dependences, eps_transitions)

        self.__add_new_start(empty_word_in_language)

    def __add_new_start(self, empty_word_in_language):
        new_term = Grammar.__search_new_nonterminal(self.nonterminals + self.alphabet,
                                                    start=self.start + '_', mode=48)
        self.nonterminals.append(new_term)
        self.rules[new_term] = Rule(new_term, (self.start,))
        self.start = new_term

        if empty_word_in_language:
            self.rules[self.start].add((EPS,))

    def __delete_unit_transitions(self):
        new_rules = copy.deepcopy(self.rules)
        for non_term_from, rule in self.rules.items():
            for transition in rule.rights:
                if len(transition) == 1 and transition[0] in self.nonterminals:
                    non_term_through = transition[0]
                    used = [non_term_from]
                    self.__compressing_transitions(non_term_from, non_term_through, new_rules, used)
                    new_rules[non_term_from].rights.remove(transition)
        self.rules = new_rules

    def __make_dependences_dict(self) -> dict[str, set]:
        dependences = dict()
        for nonterminal, rule in self.rules.items():
            for transition in rule.rights:
                for symbol in transition:
                    if symbol in self.nonterminals:
                        dependences.setdefault(symbol, set()).add(nonterminal)
        return dependences

    def __mark_non_generating_nonterminals(self):
        dependences = self.__make_dependences_dict()
        lst_no_generating_nonterminals = self.nonterminals.copy()
        queue = list(self.rules.items())
        while queue:
            nonterminal, rule = queue.pop(0)
            if nonterminal in lst_no_generating_nonterminals:
                for transition in rule.rights:
                    generating_transition = True
                    for symbol in transition:
                        generating_transition &= symbol == EPS or symbol in self.alphabet \
                                                 or symbol not in lst_no_generating_nonterminals
                    if generating_transition:
                        lst_no_generating_nonterminals.remove(nonterminal)
                        for dependent_nonterminal in dependences.get(nonterminal, set()):
                            queue.append((dependent_nonterminal, self.rules[dependent_nonterminal]))
                        break
        return lst_no_generating_nonterminals

    def __mark_eps_transitions(self, eps_transitions):
        for rule in self.rules.values():
            if (EPS,) in rule.rights:
                eps_transitions.append(rule.left)

    def __adding_new_rules_for_eps_generating(self, new_rules, eps_generating):
        for left, rule in self.rules.items():
            for transition in rule.rights:
                if len(transition) == 2:
                    if transition[0] in eps_generating:
                        if (transition[1],) not in new_rules[left].rights:
                            new_rules[left].add((transition[1],))
                    if transition[1] in eps_generating:
                        if (transition[0],) not in new_rules[left].rights:
                            new_rules[left].add((transition[0],))

    def __deleting_eps(self, dependences, eps_transitions):
        transition_eps_count = dict()
        queue = eps_transitions.copy()
        while queue:
            non_term = queue.pop(0)
            new_nonterminal = self.nonterminals.copy()
            new_rules = copy.deepcopy(self.rules)
            for transition in self.rules[non_term].rights:
                if transition == (EPS,) \
                        or transition_eps_count.setdefault((non_term,
                                                            transition), 0) == len(transition):
                    new_rules[non_term].rights.remove(transition)
            if not new_rules[non_term].rights:
                for dependent in dependences[non_term]:
                    for transition in self.rules[dependent].rights:
                        if non_term in transition:
                            new_transition = list(transition)
                            while non_term in new_transition:
                                new_transition.remove(non_term)
                            if transition in new_rules[dependent].rights:
                                new_rules[dependent].rights.remove(transition)
                            if tuple(new_transition) not in new_rules[dependent].rights:
                                new_rules[dependent].add(tuple(new_transition))
                    queue.append(dependent)
                new_nonterminal.remove(non_term)
                new_rules.pop(non_term)
            self.rules = new_rules
            self.nonterminals = new_nonterminal

    def __compressing_transitions(self, non_term_from, non_term_through, new_rules, used):
        if non_term_through in used:
            return
        used.append(non_term_through)
        for transition in new_rules[non_term_through].rights:
            if len(transition) == 2 or transition[0] in self.alphabet:
                new_rules[non_term_from].add(transition)
            elif transition[0] != non_term_from:
                self.__compressing_transitions(non_term_from, transition[0], new_rules, used)

    @staticmethod
    def __search_new_nonterminal(lst_symbols, *, start="", end="", mode=65):
        new_nonterm = ""
        shift = mode
        while start + new_nonterm + chr(shift) + end in lst_symbols:
            shift += 1
            if shift == 91:
                new_nonterm += "A"
                shift = mode
        return start + new_nonterm + chr(shift) + end