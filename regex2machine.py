from sources.DFA import NFA
import borrowing.doa2graphviz
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--regex", required=True, type=str)
parser.add_argument("--alphabet", required=False, type=str)
parser.add_argument("-doa", action='store_true')
parser.add_argument("--doa_name", required=False, default="doa_format.doa", type=str)
parser.add_argument("-graph", action='store_true')
parser.add_argument("--graph_name", required=False, default="", type=str)
args = parser.parse_args()

nfa = NFA.NFA(args.alphabet, args.regex)
if args.doa:
    nfa.translate_to_doa(args.doa_name)
    if args.graph:
        borrowing.doa2graphviz.make_graphviz(args.doa_name, args.graph_name)
