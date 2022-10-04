from sources.Machines import MinCDFA, NFA


def list_all_words(alphabet, length):
    w = [alphabet[0]]*length
    for code in range(len(alphabet)**length):
        _code = code
        for i in range(length):
            w[i] = alphabet[_code % len(alphabet)]
            _code //= len(alphabet)
        yield "".join(w)


def test_min_cdfa_make_first_classes(mocker):
    mocker.patch('sources.Machines.MinCDFA.MinCDFA._MinCDFA__new_states_and_transitions')
    mcdfa = MinCDFA.MinCDFA(doa_file='test_by_pytest/doa_texts/mincdfa_doa_pretest.doa', to_dfa=False)

    assert set(mcdfa.states) == {'0', '1'}


def test_min_cdfa_make_min():
    mcdfa = MinCDFA.MinCDFA(doa_file='test_by_pytest/doa_texts/mincdfa_doa_pretest.doa')

    assert set(mcdfa.states) == {'0', '1', '2', '3', '4', '5'}
    assert mcdfa.transitions['0']['a'] == ['1']
    assert mcdfa.transitions['1']['b'] == ['5']


def test_min_cdfa_global():
    mcdfa = MinCDFA.MinCDFA(doa_file='test_by_pytest/doa_texts/mincdfa_doa_globaltest.doa')
    nfa = NFA.NFA(doa_file='test_by_pytest/doa_texts/mincdfa_doa_globaltest.doa')
    
    for length in range(10):
        for word in list_all_words(mcdfa.alphabet, length):
            assert nfa.recognize(word) == mcdfa.recognize(word)
