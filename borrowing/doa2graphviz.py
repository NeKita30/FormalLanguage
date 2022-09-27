#!/usr/bin/python3

# by @mikhailyumanov
import sys


def parse_doa(f):
    line = f.readline().strip()
    if not line.startswith('DOA:'):
        raise Exception(f"{line} should start with 'DOA:'")


def parse_start(f):
    line = f.readline().strip()
    if not line.startswith('Start:'):
        raise Exception(f"{line} should start with 'Start:'")
    return line.split()[1]


def parse_terminal(f):
    line = f.readline().strip()
    if not line.startswith('Acceptance:'):
        raise Exception(f"{line} should start with 'Acceptance:'")

    line = line[len('Acceptance:'):]
    terminal = [state.strip() for state in line.split('&')]
    return terminal


def parse_body(f):
    lines = [line.strip() for line in f.readlines()]
    if not lines[0] == '--BEGIN--':
        raise Exception(f"Body should start with '--BEGIN--' instead of '{lines[0]}'")
    if not lines[-1] == '--END--':
        raise Exception(f"Body should end with '--END--' instead of '{lines[-1]}'")

    lines = lines[1:]
    transitions = []
    while lines:
        line = lines.pop(0)
        if line == "--END--":
            break
        elif not line.startswith('State:'):
            raise Exception(f"{line} should start with 'State:'")
        state = line.split()[1].strip()
        for i, line in enumerate(lines):
            if line.startswith('State:'):
                break
            else:
                if line == "--END--":
                    break
                elif not line.startswith('->'):
                    raise Exception(f"{line}: transition should start with '->'")
                word, to = [s.strip() for s in line.split()][1:]
                transitions.append([state, word, to])
        lines = lines[i:]

    return transitions


# modified by nekita
def make_graphviz(path_to_read: str, path_to_write: str = ""):
    if path_to_read[-4:] != ".doa":
        path_to_read += ".doa"
    with open(path_to_read, 'r') as f:
        parse_doa(f)
        start = parse_start(f)
        terminal = parse_terminal(f)
        transitions = parse_body(f)
    if path_to_write != "":
        sys.stdout = open(path_to_write, 'w')

    print("digraph {")
    for state in terminal:
        print(f"\"{state}\" [style = \"filled\"]")
    print(f"\"{start}\" [style = \"bold\"]")
    for state, word, to in transitions:
        print(f"\"{state}\" -> \"{to}\" [label = \"{word if word != 'EPS' else 'ɛ'}\"]")
    print("}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: doa2graphviz file")
    else:
        make_graphviz(sys.argv[1])
