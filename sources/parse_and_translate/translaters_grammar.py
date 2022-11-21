import sources.Grammars.errors as err
from sources.Grammars.rule import Rule
from sources.Grammars.constant import EPS


def translate_from_grm(file, grammar):
    if file[-4:] != ".grm":
        raise err.TranslateGrammarError("extension", file)

    with open(file, "r") as f:
        nonterminal_line = f.readline().strip()
        if not nonterminal_line.startswith("Nonterm.:"):
            raise err.TranslateGrammarError("non-term", nonterminal_line)
        nonterminals_set_str = nonterminal_line[9:].strip()
        nonterminals = __gen_noterminals(nonterminals_set_str)

        alphabet_line = f.readline().strip()
        if not alphabet_line.startswith("Alphabet:"):
            raise err.TranslateGrammarError("term", alphabet_line)
        alphabet_set_str = alphabet_line[9:].strip()
        alphabet = __gen_alphabet(alphabet_set_str, nonterminals)

        start_nonterminal_line = f.readline().strip()
        if not start_nonterminal_line.startswith("Start:"):
            raise err.TranslateGrammarError("start", start_nonterminal_line)
        start_nonterminal = start_nonterminal_line[6:].strip()

        if start_nonterminal not in nonterminals:
            raise err.TranslateGrammarError("unknown-non-term", start_nonterminal, nonterminals)

        for rule in f.readlines():
            if "->" not in rule:
                raise err.TranslateGrammarError("rule", rule)
            left, rights = rule.split("->")
            left = left.strip()
            rights = rights.strip().split("|")

            if left not in nonterminals:
                raise err.TranslateGrammarError("unknown-non-term", left, nonterminals)

            if left not in grammar.rules:
                grammar.rules[left] = Rule(left)

            for right_str in rights:
                if not right_str.strip():
                    raise err.TranslateGrammarError("rule", rule)
                right = __gen_right(right_str.strip(), nonterminals, alphabet)
                grammar.rules[left].add(right)
    grammar.alphabet = alphabet
    grammar.nonterminals = nonterminals
    grammar.start = start_nonterminal


def translate_to_grm(file, grammar):
    if file[-4:] != ".grm":
        raise err.TranslateGrammarError("extension", file)
    with open(file, "w") as f:
        f.write("Nonterm.: ")
        f.write(" ".join(grammar.nonterminals))
        f.write('\n')

        f.write("Alphabet: ")
        f.write(" ".join(grammar.alphabet))
        f.write('\n')

        f.write("Start: ")
        f.write(grammar.start)
        f.write('\n')

        for rule in grammar.rules.values():
            f.write(str(rule))
            f.write('\n')


def __gen_noterminals(set_str):
    set_str += " "
    nonterminals = list()
    stck = ""
    for ch in set_str:
        if ch == " ":
            if stck:
                nonterminals.append(stck)
            stck = ""
            continue
        stck += ch
    return nonterminals


def __gen_alphabet(set_str, nonterminals):
    set_str += " "
    alphabet = list()
    stck = ""
    for ch in set_str:
        if ch == " ":
            if stck:
                if stck in nonterminals:
                    raise err.TranslateGrammarError("alpha_non-term", stck)
                alphabet.append(stck)
            stck = ""
            continue
        stck += ch
    return alphabet


def __gen_right(right_str, nonterminal, alphabet):
    right = list()
    stck = ""
    stck_is_valid_symbol = False
    for ch in right_str:
        if ch == EPS:
            continue
        new_stck_is_valid_prefix = False
        new_stck_is_valid_symbol = False
        new_suff_stck_is_valid_symbol = False
        for symbol in *nonterminal, *alphabet:
            new_stck_is_valid_prefix |= symbol.startswith(stck + ch)
            new_stck_is_valid_symbol |= symbol == stck + ch
            new_suff_stck_is_valid_symbol |= symbol == ch
        if not new_stck_is_valid_prefix:
            if stck_is_valid_symbol:
                right.append(stck)
                stck = ""
                stck_is_valid_symbol = new_suff_stck_is_valid_symbol
            else:
                raise err.TranslateGrammarError("unknown-symbol", stck+ch, right_str)
        else:
            stck_is_valid_symbol = new_stck_is_valid_symbol
        stck += ch
    if stck:
        if stck_is_valid_symbol:
            right.append(stck)
        else:
            raise err.TranslateGrammarError("unknown-symbol", stck, right_str)
    return tuple(right)
