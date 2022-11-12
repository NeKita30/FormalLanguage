from sources.parse_and_translate import parsers_dfa, translaters_dfa


class NFA:
    """NFA. Can be build from regex or doa_file
    Can be translated to .doa
    Can recognize words in language"""
    def __init__(self, alphabet=None, regex="", doa_file=""):
        self.states = list()
        self.alphabet = alphabet
        self.transitions = dict()
        self.start_state = '0'
        self.accept_states = []
        if regex != "":
            self.__read_regex(regex)
        elif doa_file != "":
            self.__read_doa(doa_file)

    def __add__(self, other):
        pass

    def translate_to_doa(self, file):
        """Translate to .doa"""
        translaters_dfa.translate_to_doa(file, self.states, self.transitions, self.start_state, self.accept_states)

    def recognize(self, w, q=None, used=None):
        """Check is word w in language or not"""
        if q is None:
            q = self.start_state
        if w == "" and q in self.accept_states:
            return True
        for trans in self.transitions.get(q, []):
            for q_to in self.transitions[q][trans]:
                if w.startswith(trans):
                    if self.recognize(w[len(trans):], q_to, None):
                        return True
                if trans == 'EPS':
                    if used is None:
                        used = list()
                    if q_to not in used:
                        used.append(q)
                        if self.recognize(w, q_to, used):
                            return True
        return False

    def __read_regex(self, regex):
        """parse regex"""
        flag_check_alphabet = False
        check_alphabet = set()
        if self.alphabet is not None:
            flag_check_alphabet = True
            check_alphabet = set(self.alphabet)

        self.start_state = parsers_dfa.parse_reverse_polish(regex, flag_check_alphabet, check_alphabet,
                                                            self.accept_states,
                                                            self.states, self.transitions)
        self.alphabet = ''.join(check_alphabet)

    def __read_doa(self, file):
        """parse .doa file"""
        flag_check_alphabet = False
        check_alphabet = set()
        if self.alphabet is not None:
            flag_check_alphabet = True
            check_alphabet = set(self.alphabet)

        self.start_state = translaters_dfa.translate_from_doa(file, self.states, flag_check_alphabet,
                                                              check_alphabet, self.transitions, self.accept_states)
        self.alphabet = ''.join(check_alphabet)
