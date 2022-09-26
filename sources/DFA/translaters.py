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
            for letter in transitions.setdefault(q, []):
                for trans in transitions[q][letter]:
                    file.write(f" -> {letter} {trans}\n")
        file.write("--END--")
