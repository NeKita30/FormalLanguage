def translate_to_doa(file, states, transitions, start_state, accept_states):
    if file[-4:] != ".doa":
        file += ".doa"
    with open(file, 'w') as file:
        file.write("DOA: v1\n")

        file.write(f"Start: {start_state}\n")

        file.write("Acceptance: ")
        file.write(" &".join(accept_states))
        file.write('\n')

        file.write("--BEGIN--\n")
        for q in states:
            file.write(f"State: {q}\n")
            for letter in transitions.get(q, []):
                for trans in transitions[q][letter]:
                    file.write(f" -> {letter} {trans}\n")
        file.write("--END--")


def translate_from_doa(file, states, flag_check_alphabet, alphabet, transitions, accept_states):
    with open(file, 'r') as file:
        version = file.readline().strip()
        if not version.startswith('DOA:'):
            raise Exception(f"Should contain 'DOA:', got {version}")

        start = file.readline()
        if not start.startswith("Start:"):
            raise Exception(f"Should contain 'Start:', got {start}")
        start_state = start.split()[1]

        accept = file.readline().strip()
        if not accept.startswith('Acceptance:'):
            raise Exception(f"Should contain 'Acceptance:', got {accept}")

        accept = accept[len('Acceptance:'):]
        for state in accept.split('&'):
            if state.strip() not in accept_states:
                accept_states.append(state.strip())

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
            states.append(q)
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
                                if letter not in alphabet:
                                    raise Exception(f"Letter '{letter}' not in alphabet '{''.join(alphabet)}'")
                            else:
                                alphabet.add(letter)

                    transitions[q][word] = transitions.setdefault(q, dict()).setdefault(word, []) + [to]
    return start_state
