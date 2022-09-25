from sources.DFA import NFA


def test_rev_pol_plus():
    m1 = NFA.NFA('abcdefg', 'a b +')
    assert m1.transitions[0]['a'] == [1]
    assert m1.transitions[0]['b'] == [1]

    m2 = NFA.NFA('abcdefg', 'a b + c +')
    assert m2.transitions[2]['EPS'] == [0]
    assert m2.transitions[2]['c'] == [3]
    assert m2.transitions[0]['a'] == [1]
    assert m2.transitions[1]['EPS'] == [3]
