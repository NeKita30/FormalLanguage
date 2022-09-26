from sources.DFA import NFA


def test_rev_pol_plus():
    m1 = NFA.NFA('abcdefg', 'a b +')
    assert m1.transitions['0']['a'] == ['1']
    assert m1.transitions['0']['b'] == ['1']

    m2 = NFA.NFA('abcdefg', 'a b + c +')
    assert m2.transitions['2']['EPS'] == ['0']
    assert m2.transitions['2']['c'] == ['3']
    assert m2.transitions['0']['a'] == ['1']
    assert m2.transitions['1']['EPS'] == ['3']


def test_rev_pol_mult():
    m1 = NFA.NFA('abcdefg', 'a b *')
    assert m1.transitions['2']['a'] == ['0']
    assert m1.transitions['0']['b'] == ['1']

    m2 = NFA.NFA('abcdefg', 'a b + c *')
    assert m2.transitions['1']['EPS'] == ['2']
    assert m2.transitions['2']['c'] == ['3']
    assert m2.transitions['0']['a'] == ['1']
    assert m2.transitions['0']['b'] == ['1']

    m3 = NFA.NFA('abcdefg', 'c a b + *')
    assert m3.transitions['2']['c'] == ['0']
    assert m3.transitions['0']['a'] == ['1']
    assert m3.transitions['0']['b'] == ['1']

    m4 = NFA.NFA('abcdefg', 'a b + c d + *')
    assert m4.transitions['1']['EPS'] == ['2']
    assert m4.transitions['0']['a'] == ['1']
    assert m4.transitions['0']['b'] == ['1']
    assert m4.transitions['2']['c'] == ['3']
    assert m4.transitions['2']['d'] == ['3']


def test_rev_pol_kleene_plus():
    m1 = NFA.NFA('abcdefg', 'a ^+')
    assert m1.transitions['0']['a'] == ['1']
    assert m1.transitions['1']['EPS'] == ['0']

    m2 = NFA.NFA('abcdefg', 'c a b + * ^+')
    assert m2.transitions['2']['c'] == ['0']
    assert m2.transitions['0']['a'] == ['1']
    assert m2.transitions['0']['b'] == ['1']
    assert m2.transitions['1']['EPS'] == ['2']


def test_rev_pol_kleene_star():
    m1 = NFA.NFA('abcdefg', 'a ^*')
    assert m1.transitions['0']['a'] == ['0']

    m2 = NFA.NFA('abcdefg', 'a b * c + ^*')
    assert m2.transitions['2']['a'] == ['0']
    assert m2.transitions['0']['b'] == ['1']
    assert m2.transitions['3']['EPS'] == ['2']
    assert m2.transitions['3']['c'] == ['4']
    assert m2.transitions['4']['EPS'] in [['3', '6'], ['6', '3']]
    assert m2.transitions['5']['EPS'] in [['3', '6'], ['6', '3']]
