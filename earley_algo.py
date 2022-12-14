from sources.Grammars import Grammar, Earley
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--grammar", required=True, type=str, help=".grm file with grammar description")
parser.add_argument("-notstart", action="store_true", help="not add new start nonterminal")

args = parser.parse_args()
grm = Grammar(args.grammar)
early = Earley(grm, not args.notstart)

print("Type Cntr+D to exit")
while True:
    try:
        word = input("Word: ")
    except EOFError:
        break
    if early.check_word_occurrence(word):
        print(f"Word {word} belongs to given language")
    else:
        print(f"Word {word} does not belongs to language")
