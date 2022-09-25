from sources.DFA import parsers


class NFA:
    def __init__(self, alphabet, regular=""):
        self.states = list()
        self.alphabet = alphabet
        self.transitions = dict()
        self.start_state = 0
        self.accept_states = []
        self.__parsing(regular)
        pass

    def __add__(self, other):
        pass

    def present(self):
        pass

    def recognize(self, w):
        pass

    def __parsing(self, regular):
        self.start_state = parsers.parse_reverse_polish(regular, self.accept_states,
                                                        self.states, self.transitions)
