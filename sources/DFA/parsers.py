def parse_reverse_polish(regex, flag_check_alphabet, alphabet, accept_states,
                         states, transitions):
    operators = ('+', '*', '^+', '^*')
    degrees = ('^' + str(i) for i in range(100))
    operands_and_operators = regex.split()
    states_cnt = 0

    stack = []
    for item in operands_and_operators:
        if item not in operators and item not in degrees:
            if item != 'EPS':
                for letter in item:
                    if flag_check_alphabet:
                        if letter not in alphabet:
                            raise Exception(f"Letter '{letter}' not in alphabet '{''.join(alphabet)}'")
                    else:
                        alphabet.add(letter)
            stack.append(item)
        else:
            result_states = [None, None]
            if item == '+':
                states_cnt += operator_plus(states, stack, states_cnt, transitions, result_states)
            elif item == '*':
                states_cnt += operator_mult(states, stack, states_cnt, transitions, result_states)
            elif item == '^+':
                states_cnt += operator_kleene_plus(states, stack, states_cnt, transitions, result_states)
            elif item == '^*':
                states_cnt += operator_kleene_star(states, stack, states_cnt, transitions, result_states)
            stack.append(tuple(result_states))
    if len(stack) > 1:
        raise Exception(f"Error during parsing regex '{regex}', unparsed: {stack}")
    if not isinstance(stack[0], tuple):
        transitions[str(states_cnt)] = dict()
        transitions[str(states_cnt)][stack.pop()] = [str(states_cnt + 1)]
        states.append(str(states_cnt))
        states.append(str(states_cnt + 1))
        stack.append((str(states_cnt), str(states_cnt + 1)))
    start, end = stack.pop()
    accept_states.append(end)
    return start


def operator_plus(states, stack, states_cnt, transitions, result_states):
    states.append(str(states_cnt))
    states.append(str(states_cnt + 1))
    for i in range(2):
        operand = stack.pop()
        if isinstance(operand, str):
            transitions[str(states_cnt)][operand] = \
                transitions.setdefault(str(states_cnt), dict()).setdefault(operand, []) + [str(states_cnt + 1)]
        else:
            state_enter, state_exit = operand
            transitions[str(states_cnt)]['EPS'] = \
                transitions.setdefault(str(states_cnt), dict()).setdefault('EPS', []) + [str(state_enter)]
            transitions[state_exit]['EPS'] = \
                transitions.setdefault(str(state_exit), dict()).setdefault('EPS', []) + [str(states_cnt + 1)]
    result_states[0] = str(states_cnt)
    result_states[1] = str(states_cnt + 1)
    return 2


def operator_mult(states, stack, states_cnt, transitions, result_states):
    right_operand = stack.pop()
    left_operand = stack.pop()
    states_cnt_delta = 0
    if isinstance(right_operand, str):
        states.append(str(states_cnt))
        states.append(str(states_cnt + 1))
        transitions[str(states_cnt)][right_operand] = \
            transitions.setdefault(str(states_cnt),
                                   dict()).setdefault(right_operand, []) + [str(states_cnt + 1)]
        result_states[1] = str(states_cnt + 1)
        merge_state = str(states_cnt)
        states_cnt_delta = 2
    else:
        state_enter, state_exit = right_operand
        result_states[1] = state_exit
        merge_state = state_enter
    if isinstance(left_operand, str):
        states.append(str(states_cnt + states_cnt_delta))
        transitions[str(states_cnt + states_cnt_delta)][left_operand] = \
            transitions.setdefault(str(states_cnt + states_cnt_delta),
                                   dict()).setdefault(left_operand, []) + [merge_state]
        result_states[0] = str(states_cnt + states_cnt_delta)
        states_cnt_delta += 1
    else:
        state_enter, state_exit = left_operand
        result_states[0] = str(state_enter)
        transitions[state_exit]['EPS'] = \
            transitions.setdefault(state_exit, dict()).setdefault('EPS', []) + [merge_state]
    return states_cnt_delta


def operator_kleene_plus(states, stack, states_cnt, transitions, result_states):
    operand = stack.pop()
    if isinstance(operand, str):
        states.append(str(states_cnt))
        states.append(str(states_cnt + 1))
        transitions[str(states_cnt)][operand] = \
            transitions.setdefault(str(states_cnt), dict()).setdefault(operand, []) + [str(states_cnt + 1)]
        transitions[str(states_cnt + 1)]['EPS'] = \
            transitions.setdefault(str(states_cnt + 1), dict()).setdefault('EPS', []) + [str(states_cnt)]
        result_states[0] = str(states_cnt)
        result_states[1] = str(states_cnt + 1)
        return 2
    else:
        state_enter, state_exit = operand
        transitions[state_exit]['EPS'] = \
            transitions.setdefault(state_exit, dict()).setdefault('EPS', []) + [state_enter]
        result_states[0] = state_enter
        result_states[1] = state_exit
        return 0


def operator_kleene_star(states, stack, states_cnt, transitions, result_states):
    operand = stack.pop()
    if isinstance(operand, str):
        states.append(str(states_cnt))
        transitions[str(states_cnt)][operand] = \
            transitions.setdefault(str(states_cnt), dict()).setdefault(operand, []) + [str(states_cnt)]
        result_states[0] = str(states_cnt)
        result_states[1] = str(states_cnt)
        return 1
    else:
        state_enter, state_exit = operand
        states.append(str(states_cnt))
        states.append(str(states_cnt + 1))
        transitions[str(states_cnt)]['EPS'] = \
            transitions.setdefault(str(states_cnt), dict()).setdefault('EPS', []) + [state_enter]
        transitions[state_exit]['EPS'] = \
            transitions.setdefault(state_exit, dict()).setdefault('EPS', []) + [state_enter]
        transitions[state_exit]['EPS'] = \
            transitions.setdefault(state_exit, dict()).setdefault('EPS', []) + [str(states_cnt + 1)]
        transitions[str(states_cnt)]['EPS'] = \
            transitions.setdefault(str(states_cnt), dict()).setdefault('EPS', []) + [str(states_cnt + 1)]
        result_states[0] = str(states_cnt)
        result_states[1] = str(states_cnt + 1)
        return 2
