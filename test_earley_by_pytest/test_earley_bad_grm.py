from sources.Grammars import Grammar, Earley


def test_earley_bad_grm():
    grm = Grammar('test_earley_by_pytest/grm_bad_earley.grm')
    early = Earley(grm)
    assert not early.check_word_occurrence("hello")
    assert early.check_word_occurrence("")
    assert not early.check_word_occurrence("abc")
    assert early.check_word_occurrence("aaacbccbcbbbcbc")
