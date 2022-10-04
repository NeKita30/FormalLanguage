from sources.Machines import DFA


def test_dfa_recognize():
    dfa = DFA.DFA(doa_file="test_by_pytest/doa_texts/dfa_test_recognize.doa")
    dfa.make_complete_dfa()

    assert dfa.recognize("abf")
    assert dfa.recognize("cddddcf")
    assert dfa.recognize("cddde")
    assert dfa.recognize("")
    assert not dfa.recognize("af")
    assert not dfa.recognize("afbb")
    assert not dfa.recognize("cdef")
    assert not dfa.recognize("abxyz")
