from sources.Machines import DFA


def test_dfa_determ_one(mocker):
    mocker.patch('sources.Machines.DFA.DFA._DFA__make_one_letter_transitions')
    mocker.patch('sources.Machines.DFA.DFA._DFA__dfs_deleting_unreached')

    dfa = DFA.DFA(alphabet='ab', doa_file="test_by_pytest/doa_texts/dfa_test_determ.doa")

    assert set(dfa.states) == {'0', '1', '2', '3', '4', '5', '6', '1_2', '4_6', '5_6', '2_4_6', '4_5_6'}
    assert dfa.transitions['0'] == {'a': ['1_2'], 'b': ['3']}
    assert dfa.transitions['2_4_6']['a'] == ['4_5_6']
    assert dfa.transitions['5_6']['b'] == []
    assert set(dfa.accept_states) == {'1', '4', '5', '1_2', '4_6', '5_6', '2_4_6', '4_5_6'}


def test_dfa_completes():
    dfa = DFA.DFA(alphabet='ab', doa_file="test_by_pytest/doa_texts/dfa_test_determ.doa")

    assert set(dfa.states) == {'0', '3', '4', '5', '1_2', '4_6', '5_6', '2_4_6', '4_5_6'}
    assert set(dfa.accept_states) == {'4', '5', '1_2', '4_6', '5_6', '2_4_6', '4_5_6'}

    dfa.make_complete_dfa()

    assert set(dfa.states) == {'0', '3', '4', '5', '1_2', '4_6', '5_6', '2_4_6', '4_5_6', 'X'}
    assert dfa.transitions['5_6']['a'] == ['X']

    dfa = DFA.DFA(alphabet="ab", doa_file="test_by_pytest/doa_texts/dfa_test_unusual.doa", to_dfa=False)
    dfa.make_complete_dfa()
    assert set(dfa.states) == {'0', '1', 'X', 'XX'}
    assert set(dfa.transitions['0']['b']) == {'XX',}
    assert set(dfa.transitions['X']['b']) == {'XX',}
    assert set(dfa.transitions['XX']['a']) == {'XX',}


def test_dfa_determ_two(mocker):
    dfa = DFA.DFA(alphabet='ab', doa_file="test_by_pytest/doa_texts/dfa_test_determ_unchanged.doa")
    dfa.make_complete_dfa()
    assert set(dfa.states) == {'0', '1', '2', '3'}
