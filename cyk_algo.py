from sources.Grammars import Grammar, CockeYoungerKasami
import argparse
import fileinput
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--grammar", required=True, type=str, help=".grm file with grammar description")
parser.add_argument("-cnf", action="store_true", help="do not convert to chomsky normal form")

args = parser.parse_args()
grm = Grammar(args.grammar)
cyk = CockeYoungerKasami(grm, convert_to_chomsky=not args.cnf)

print("Type Cntr+D to exit")
while True:
    try:
        word = input("Word: ")
    except EOFError:
        break
    if cyk.check_word_occurrence(word):
        print(f"Word {word} belongs to given language")
    else:
        print(f"Word {word} does not belongs to language")
