def parse_reverse_polish(regular, accept_states,
                         states, transitions):
    operators = ('+', '*', '^+', '^*')
    degrees = ('^' + str(i) for i in range(100))
    operands_and_operators = regular.split()
    states_cnt = 0

    stack = []
    for item in operands_and_operators:
        if item not in operators and item not in degrees:
            stack.append(item)
        else:
            if item == '+':
                states.append(str(states_cnt))
                states.append(str(states_cnt + 1))
                for i in range(2):
                    word = stack.pop()
                    if isinstance(word, str):
                        transitions[states_cnt][word] = \
                            transitions.setdefault(states_cnt, dict()).setdefault(word, []) + [states_cnt + 1]
                    else:
                        state_enter, state_exit = word
                        transitions[states_cnt]['EPS'] = \
                            transitions.setdefault(states_cnt, dict()).setdefault('EPS', []) + [state_enter]
                        transitions[state_exit]['EPS'] = \
                            transitions.setdefault(state_exit, dict()).setdefault('EPS', []) + [states_cnt + 1]
                stack.append((states_cnt, states_cnt + 1))
                states_cnt += 2
    start, end = stack.pop()
    accept_states.append(end)
    return start
