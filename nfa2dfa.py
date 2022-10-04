from sources.Machines import NFA, DFA, MinCDFA
import borrowing.doa2graphviz
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("--alphabet", required=False, default=None, type=str, help="Alphabet")
parser.add_argument("--nfa_doa", required=True, type=str, help="NFA .doa file")
parser.add_argument("-cdfa", action='store_true', help="To make CDFA")
parser.add_argument("-mincdfa", action='store_true', help="To make MinCDFA")
parser.add_argument("--dfa_doa", required=False, default="doa_formatп.doa", type=str, help="Name of .doa output file")
parser.add_argument("-graph", action='store_true', help="To make graphviz")
parser.add_argument("--graph_name", required=False, default="", type=str,
                    help="Name of graphviz output file, requires -graph. By default writes in terminal")
args = parser.parse_args()

if args.mincdfa:
    dfa = MinCDFA.MinCDFA(alphabet=args.alphabet, doa_file=args.nfa_doa)
else:
    dfa = DFA.DFA(alphabet=args.alphabet, doa_file=args.nfa_doa)

if args.cdfa:
    dfa.make_complete_dfa()

dfa.translate_to_doa(args.dfa_doa)

if args.graph:
    borrowing.doa2graphviz.make_graphviz(args.dfa_doa, args.graph_name)
