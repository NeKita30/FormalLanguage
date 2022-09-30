from sources.Machines import DFA
import copy


class MinCDFA(DFA.DFA):
    def __init__(self, alphabet=None, regular="", doa_file="", to_dfa=True):
        super().__init__(alphabet, regular, doa_file, to_dfa)
        self.make_complete_dfa()
        self.__make_min()

    def __make_min(self):
        states = dict()
        new_states = dict.fromkeys(self.states, '0')
        new_transitions = copy.deepcopy(self.transitions)
        self.__make_first_classes(new_states)

        while states != new_states:
            states = copy.deepcopy(new_states)
            self.__new_states_and_transitions(states, new_states, new_transitions)
        self.transitions = {states[state]: {letter: new_transitions[state][letter]
                                            for letter in self.alphabet}
                            for state in self.states}
        self.states = list(set(states.values()))
        self.start_state = states[self.start_state]
        self.accept_states = list(set([states[q_f] for q_f in self.accept_states]))

    def __new_states_and_transitions(self, old_states, new_states, new_transitions):
        cnt = 0
        lst_id = dict()
        for state in self.states:
            state_id = (new_states[state],)
            for i, letter in enumerate(self.alphabet):
                new_transitions[state][letter] = [old_states[self.transitions[state][letter][0]]]
                state_id += (new_transitions[state][letter][0],)
            if state_id not in lst_id:
                lst_id[state_id] = str(cnt)
                cnt += 1
            new_states[state] = lst_id[state_id]

    def __make_first_classes(self, new_states):
        for q in self.accept_states:
            new_states[q] = '1'
