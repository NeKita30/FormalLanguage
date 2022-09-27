from sources.DFA import NFA, DFA
import borrowing.doa2graphviz
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--regex", required=True, type=str)
parser.add_argument("--alphabet", required=False, type=str)
parser.add_argument("-doa", action='store_true')
parser.add_argument("-one_nka", action='store_true')
parser.add_argument("--doa_name", required=False, default="doa_format.doa", type=str)
parser.add_argument("-graph", action='store_true')
parser.add_argument("--graph_name", required=False, default="", type=str)
args = parser.parse_args()

args.doa_name = os.path.join(os.getcwd(), args.doa_name)
if args.one_nka:
    machine = DFA.DFA(args.alphabet, args.regex)
else:
    machine = NFA.NFA(args.alphabet, args.regex)

if args.doa:
    machine.translate_to_doa(args.doa_name)
    if args.graph:
        borrowing.doa2graphviz.make_graphviz(args.doa_name, args.graph_name)
