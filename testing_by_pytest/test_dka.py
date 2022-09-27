from sources.DFA import DFA


def test_dka_1_0_letter(mocker):
    mocker.patch('sources.DFA.DFA.DFA._DFA__compress_eps_transitions')
    mocker.patch('sources.DFA.DFA.DFA._DFA__delete_eps_transitions')
    mocker.patch('sources.DFA.DFA.DFA._DFA__make_determined')
    dfa = DFA.DFA(doa_file="testing_by_pytest/doa_texts/dka_test_first.doa")
    assert 'a' in dfa.transitions['0']
    x = dfa.transitions['0']['a'][0]
    assert 'b' in dfa.transitions[x]
    assert 'c' in dfa.transitions['0']
    x = dfa.transitions['0']['c'][0]
    assert 'd' in dfa.transitions[x]

    assert 'a' in dfa.transitions['1']
    assert dfa.transitions['1']['a']
    assert dfa.transitions['2']['d'] == ['4']
    assert dfa.transitions['3']['EPS'] == ['4']
    assert len(dfa.states) == 17


def test_dka_compress_eps(mocker):
    mocker.patch('sources.DFA.DFA.DFA._DFA__delete_eps_transitions')
    mocker.patch('sources.DFA.DFA.DFA._DFA__make_determined')
    dfa = DFA.DFA(doa_file="testing_by_pytest/doa_texts/dka_test_second.doa")
    assert set(dfa.transitions['0']['EPS']) == {'1', '3', '2'}
    assert set(dfa.transitions['4']['EPS']) == {'5', '8', '9', '11', '12', '6', '7', '10'}
    assert set(dfa.transitions['5']['EPS']) == {'8', '9', '11', '12', '6', '7', '10', '5'}
    assert set(dfa.transitions['6']['EPS']) == {'7', '10'}
    assert set(dfa.transitions['8']['EPS']) == {'9', '11', '12'}
    assert set(dfa.transitions['10']['EPS']) == {'6', '7'}
    assert set(dfa.transitions['11']['EPS']) == {'12', '8', '9'}
    assert set(dfa.transitions['12']['EPS']) == {'8', '9', '11'}

    assert set(dfa.accept_states) == {'0', '1', '2', '4', '5', '8', '9', '11', '12'}


def test_dka_deleting(mocker):
    mocker.patch('sources.DFA.DFA.DFA._DFA__make_determined')
    dfa = DFA.DFA(doa_file="testing_by_pytest/doa_texts/dka_test_third.doa")
    assert set(dfa.transitions['0']['a']) == {'2', '5'} and set(dfa.transitions['0'].keys()) == {'a'}
    assert set(dfa.transitions['3'].keys()) == set()
    assert set(dfa.transitions['5']['a']) == {'9', '13'}
    assert set(dfa.transitions['5']['c']) == {'7', '11'}
    assert set(dfa.transitions['7']['c']) == {'7', '11'}
    assert set(dfa.transitions['7']['a']) == {'9', '13'}

    assert set(dfa.states) == {'0', '2', '3', '5', '9', '7', '11', '13'}
    assert set(dfa.accept_states) == {'3', '5', '11', '7', '13'}
