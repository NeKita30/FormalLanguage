from sources.Machines import MinCDFA


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


