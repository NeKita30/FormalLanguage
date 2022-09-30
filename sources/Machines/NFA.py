from sources.parse_and_translate import parsers, translaters


class NFA:
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
        translaters.translate_to_doa(file, self.states, self.transitions, self.start_state, self.accept_states)

    def recognize(self, w):
        pass

    def __read_regex(self, regex):
        flag_check_alphabet = False
        check_alphabet = set()
        if self.alphabet is not None:
            flag_check_alphabet = True
            check_alphabet = set(self.alphabet)

        self.start_state = parsers.parse_reverse_polish(regex, flag_check_alphabet, check_alphabet, self.accept_states,
                                                        self.states, self.transitions)
        self.alphabet = ''.join(check_alphabet)

    def __read_doa(self, file):
        flag_check_alphabet = False
        check_alphabet = set()
        if self.alphabet is not None:
            flag_check_alphabet = True
            check_alphabet = set(self.alphabet)

        self.start_state = translaters.translate_from_doa(file, self.states, flag_check_alphabet,
                                                          check_alphabet, self.transitions, self.accept_states)
        self.alphabet = ''.join(check_alphabet)
