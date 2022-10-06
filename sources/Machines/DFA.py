from sources.Machines import NFA
import copy


class DFA(NFA.NFA):
    """DFA. Can be build as NFA, in both ways
    Can be made completed
    Can recognize words (another implementation)
    """
    def __init__(self, alphabet=None, regular="", doa_file="", to_dfa=True, study_mode=""):
        super().__init__(alphabet, regular, doa_file)
        if to_dfa:
            self.__make_dfa(study_mode)

    def recognize(self, w, q=None, used=None):
        """Check is word w in language or not"""
        q = self.start_state
        for letter in w:
            if letter not in self.alphabet:
                break
            q = self.transitions[q][letter][0]
        else:
            return q in self.accept_states
        return False

    def __make_dfa(self, study_mode):
        """Make DFA
        NFA -> 1-letter NFA, Tompson's alg."""
        self.__make_one_letter_transitions(study_mode)
        self.__make_determined()
        if study_mode:
            self.translate_to_doa(study_mode+"/DFA.doa")

    def __make_one_letter_transitions(self, study_mode):
        """Make <=1-letter NFA, then 1-letter NFA"""
        self.__make_one_or_zero_letter_transitions()
        if study_mode:
            self.translate_to_doa(study_mode+"/one_zero_letter_NFA.doa")
        self.__compress_eps_transitions()
        self.__delete_eps_transitions()
        if study_mode:
            self.translate_to_doa(study_mode+"/one_letter_NFA.doa")

    def __make_determined(self):
        """Tompson's alg."""
        for q in self.states:
            if q not in self.transitions:
                self.transitions[q] = dict()

        new_states = self.states.copy()
        new_accept_states = self.accept_states.copy()
        states_to_add_in_tompson_table = list()
        tompson = dict()

        for state in self.states:
            tompson[state] = dict()
            for letter in self.alphabet:
                if letter in self.transitions[state]:
                    new_state = "_".join(sorted(self.transitions[state][letter]))
                    tompson[state][letter] = [new_state]
                    if new_state not in states_to_add_in_tompson_table and new_state not in new_states:
                        states_to_add_in_tompson_table.append(new_state)
                        new_states.append(new_state)
                else:
                    tompson[state][letter] = []
        while states_to_add_in_tompson_table:
            state = states_to_add_in_tompson_table[0]
            tompson[state] = dict()
            states_included = state.split('_')
            for letter in self.alphabet:
                result = ""
                for sub_state in states_included:
                    if tompson[sub_state][letter]:
                        if result:
                            result += '_'
                        result += tompson[sub_state][letter][0]
                result = '_'.join(sorted(set(result.split('_'))))
                result = None if result == "" else result
                if result is not None and result not in states_to_add_in_tompson_table and result not in new_states:
                    states_to_add_in_tompson_table.append(result)
                    new_states.append(result)
                tompson[state][letter] = list()
                if result:
                    tompson[state][letter] = [result]
            states_to_add_in_tompson_table.pop(0)
        self.transitions = tompson
        for accept in self.accept_states:
            for new_state in new_states:
                if accept in new_state.split('_') and new_state not in new_accept_states:
                    new_accept_states.append(new_state)

        self.accept_states = new_accept_states
        self.__dfs_deleting_unreached(tompson, new_states)
        self.transitions = tompson
        self.states = new_states

    def make_complete_dfa(self, study_mode=""):
        """Make DFA completed, adding 'trash' state"""
        flag_added_new_ways = False
        trsh = 'X'
        while trsh in self.states:
            trsh += 'X'
        self.states.append(trsh)
        self.transitions[trsh] = dict()
        for q in self.states:
            for letter in self.alphabet:
                if not self.transitions.setdefault(q, dict()).setdefault(letter, []):
                    flag_added_new_ways |= q != trsh
                    self.transitions[q][letter] = [trsh]
        if not flag_added_new_ways:
            self.states.pop()
            self.transitions.popitem()
        if study_mode:
            self.translate_to_doa(study_mode+"/CDFA.doa")

    def __make_one_or_zero_letter_transitions(self):
        """NFA -> <=1-letter NFA"""
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
        """To compress EPS ways"""
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
        """Helper function, used for searching and compressing all EPS ways from q_from"""
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
        """Deleting EPS ways, replacing them with 1-letter transitions"""
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

        new_states = self.states.copy()
        self.__dfs_deleting_unreached(new_transitions, new_states)
        self.transitions = new_transitions
        self.states = new_states

    def __dfs_deleting_unreached(self, transitions, states):
        """Searching unreached states to delete"""
        used = list()
        self.__dfs_for_deleting(used, transitions, self.start_state)
        _states = states.copy()
        for q in _states:
            if q not in used:
                states.remove(q)
                if q in self.accept_states:
                    self.accept_states.remove(q)
                if transitions.get(q, False):
                    transitions.pop(q)

    def __dfs_for_deleting(self, used, transitions, q):
        """Helper function. dfs from self.start"""
        used.append(q)
        if transitions.get(q, False):
            for letter in transitions[q]:
                for p in transitions[q][letter]:
                    if p not in used:
                        self.__dfs_for_deleting(used, transitions, p)
