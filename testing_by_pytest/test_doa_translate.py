from sources.DFA import NFA


def test_doa_trans():
    m = NFA.NFA("abcdefg", "a b + c * ^* a b + c * *")
    m.translate_to_doa("borrowing/popyt.doa")
