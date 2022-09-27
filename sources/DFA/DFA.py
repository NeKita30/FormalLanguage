from sources.DFA import translaters
from sources.DFA import NFA
import copy


class DFA(NFA.NFA):
    def __init__(self, alphabet=None, regular="", doa_file=""):
        super().__init__(alphabet, regular, doa_file)
        self.__make_dka()

    def __make_dka(self):
        self.__make_one_letter_transitions()
        self.__make_determined()

    def __make_one_letter_transitions(self):
        self.__make_one_or_zero_letter_transitions()
        self.__compress_eps_transitions()
        self.__delete_eps_transitions()

    def __make_determined(self):
        pass

    def __make_one_or_zero_letter_transitions(self):
        state_cnt = len(self.states)
        new_transitions = copy.deepcopy(self.transitions)
        new_states = self.states.copy()
        for q in self.states:
            list_words = list(self.transitions.setdefault(q, dict()).keys())
            for word in list_words:
                if word != "EPS" and len(word) > 1:
                    for end_of_trans in self.transitions[q][word]:
                        new_states.append(str(state_cnt))
                        new_transitions[q][word[0]] = \
                            new_transitions[q].setdefault(word[0], []) + [str(state_cnt)]
                        state_cnt += 1
                        for letter in word[1:-1]:
                            new_states.append(str(state_cnt))
                            new_transitions[str(state_cnt - 1)][letter] = \
                                new_transitions.setdefault(str(state_cnt - 1),
                                                           dict()).setdefault(letter, []) + [str(state_cnt)]
                            state_cnt += 1
                        new_transitions[str(state_cnt - 1)][word[-1]] = \
                            new_transitions.setdefault(str(state_cnt - 1),
                                                       dict()).setdefault(word[-1], []) + [end_of_trans]
                    new_transitions[q].pop(word)
        self.states = new_states
        self.transitions = new_transitions

    def __compress_eps_transitions(self):
        new_transitions = copy.deepcopy(self.transitions)
        for q_start in self.states:
            accept_start = False
            used = [q_start]
            if 'EPS' in self.transitions.setdefault(q_start, dict()):
                for q_sep in self.transitions[q_start]['EPS']:
                    accept_sep = q_sep in self.accept_states
                    if q_sep not in used:
                        used.append(q_sep)
                        if 'EPS' in self.transitions.setdefault(q_sep, dict()):
                            for q_end in self.transitions[q_sep]['EPS']:
                                if q_end not in used:
                                    accept_sep |= self.__compressing(q_start, q_end, new_transitions, used)
                    accept_start |= accept_sep
            if accept_start:
                self.accept_states.append(q_start)
        self.transitions = new_transitions

    def __compressing(self, q_from, q_to, transitions, used):
        transitions[q_from]['EPS'] += [q_to]
        used.append(q_to)
        accept = q_to in self.accept_states
        if 'EPS' in transitions.setdefault(q_to, dict()):
            list_qs = list(transitions[q_to]['EPS'])
            for q in list_qs:
                if q not in used:
                    accept |= self.__compressing(q_from, q, transitions, used)
        return accept

    def __delete_eps_transitions(self):
        new_transitions = copy.deepcopy(self.transitions)
        for q_from in self.transitions:
            if 'EPS' in self.transitions[q_from]:
                for q_sep in self.transitions[q_from]['EPS']:
                    if q_sep != q_from:
                        for letter in self.transitions.get(q_sep, []):
                            if letter != 'EPS':
                                for q_to in self.transitions[q_sep][letter]:
                                    new_transitions[q_from][letter] = \
                                        new_transitions[q_from].setdefault(letter, []) + [q_to]
                    new_transitions[q_from]['EPS'].remove(q_sep)
                new_transitions[q_from].pop('EPS')

        used = list()
        self.__dfs_deleting_unreached(used, new_transitions, self.start_state)
        new_states = self.states.copy()
        for q in self.states:
            if q not in used:
                new_states.remove(q)
                if q in self.accept_states:
                    self.accept_states.remove(q)
                if new_transitions.get(q, False):
                    new_transitions.pop(q)

        self.transitions = new_transitions
        self.states = new_states

    def __dfs_deleting_unreached(self, used, transitions, q):
        used.append(q)
        if transitions.get(q, False):
            for letter in transitions[q]:
                for p in transitions[q][letter]:
                    if p not in used:
                        self.__dfs_deleting_unreached(used, transitions, p)
