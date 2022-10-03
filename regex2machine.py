from sources.Machines import NFA, DFA, MinCDFA
import borrowing.doa2graphviz
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--regex", required=True, type=str)
parser.add_argument("--alphabet", required=False, type=str)
parser.add_argument("-doa", action='store_true')
parser.add_argument("-dfa", action='store_true')
parser.add_argument("-cdfa", action='store_true')
parser.add_argument("-mincdfa", action='store_true')
parser.add_argument("-study_mode", default="", type=str)
parser.add_argument("--doa_name", required=False, default="doa_format.doa", type=str)
parser.add_argument("-graph", action='store_true')
parser.add_argument("--graph_name", required=False, default="", type=str)
args = parser.parse_args()

args.doa_name = os.path.join(os.getcwd(), args.doa_name)
if args.mincdfa:
    machine = MinCDFA.MinCDFA(args.alphabet, args.regex)
elif args.dfa or args.cdfa:
    machine = DFA.DFA(args.alphabet, args.regex, study_mode=args.study_mode)
    if args.cdfa:
        machine.make_complete_dfa(study_mode=args.study_mode)
else:
    machine = NFA.NFA(args.alphabet, args.regex)

if args.doa:
    machine.translate_to_doa(args.doa_name)
    if args.graph:
        borrowing.doa2graphviz.make_graphviz(args.doa_name, args.graph_name)
