from sources.DFA import parsers
from sources.DFA import translaters


class NFA:
    def __init__(self, alphabet="", regular=""):
        self.states = list()
        self.alphabet = alphabet
        self.transitions = dict()
        self.start_state = '0'
        self.accept_states = []
        self.__parsing(regular)

    def __add__(self, other):
        pass

    def translate_to_doa(self, file):
        translaters.translate_to_doa(file, self.states, self.transitions, self.start_state, self.accept_states)

    def recognize(self, w):
        pass

    def __parsing(self, regular):
        self.start_state = parsers.parse_reverse_polish(regular, self.accept_states,
                                                        self.states, self.transitions)
