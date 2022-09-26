from sources.DFA import NFA


def test_doa_trans():
    m = NFA.NFA("abcdefg", "ab ^+ aab ^+ *")
    m.translate_to_doa("borrowing/popyt.doa")
