from sources.Machines import NFA


def test_nfa_recognize_first():
    nfa = NFA.NFA(alphabet="abc", regex="ab ^+ aab ^+ *")
    assert nfa.recognize("abababaabaab")
    assert not nfa.recognize("ab")
    assert not nfa.recognize("aab")
    assert not nfa.recognize("ababcaab")


def test_nfa_recognize_second():
    nfa = NFA.NFA(doa_file="test_by_pytest/doa_texts/nfa_test_recognize")
    assert not nfa.recognize("aa")
    assert nfa.recognize("baaaa")
    assert not nfa.recognize("b")
    assert not nfa.recognize("ac")
    assert nfa.recognize("baaac")
