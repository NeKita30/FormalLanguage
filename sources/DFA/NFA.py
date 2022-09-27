from sources.DFA import parsers
from sources.DFA import translaters


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
        with open(file, 'r') as file:
            flag_check_alphabet = False
            if self.alphabet is not None:
                flag_check_alphabet = True
            else:
                self.alphabet = ""

            version = file.readline().strip()
            if not version.startswith('DOA:'):
                raise Exception(f"Should contain 'DOA:', got {version}")

            start = file.readline()
            if not start.startswith("Start:"):
                raise Exception(f"Should contain 'Start:', got {start}")
            self.start_state = start.split()[1]

            accept = file.readline().strip()
            if not accept.startswith('Acceptance:'):
                raise Exception(f"Should contain 'Acceptance:', got {accept}")

            accept = accept[len('Acceptance:'):]
            self.accept_states = [state.strip() for state in accept.split('&')]
            self.accept_states = list(set(self.accept_states))

            lines = [line.strip() for line in file.readlines()]
            if not lines[0] == '--BEGIN--':
                raise Exception(f"Should contain '--BEGIN--', got {lines[0]}")
            if not lines[-1] == '--END--':
                raise Exception(f"Should contain '--END--', got {lines[-1]}")
            lines.pop(0)
            while lines[:-1]:
                line = lines.pop(0)
                if not line.startswith('State:'):
                    raise Exception(f"Transitions description should start with 'State:', got {line}")
                q = line.split()[1].strip()
                self.states.append(q)
                while lines[:-1]:
                    if lines[0].startswith('State:'):
                        break
                    else:
                        line = lines.pop(0)
                        if not line.startswith('->'):
                            raise Exception(f"Transitions description should contain '->, got {line}'")
                        word, to = [s.strip() for s in line.split()][1:]
                        if word != 'EPS':
                            for letter in word:
                                if flag_check_alphabet:
                                    if letter not in self.alphabet:
                                        raise Exception(f"Letter '{letter}' not in alphabet '{self.alphabet}'")
                                else:
                                    self.alphabet += letter

                        self.transitions[q][word] = self.transitions.setdefault(q, dict()).setdefault(word, []) + [to]
