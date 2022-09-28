from sources.DFA import DFA


def test_dfa_determ_one(mocker):
    def replace_make_one_letter(self):
        for q in self.states:
            if q not in self.transitions:
                self.transitions[q] = dict()

    mocker.patch('sources.DFA.DFA.DFA._DFA__make_one_letter_transitions', replace_make_one_letter)
    mocker.patch('sources.DFA.DFA.DFA._DFA__dfs_deleting_unreached')

    dfa = DFA.DFA(alphabet='ab', doa_file="test_by_pytest/doa_texts/dfa_test_determ.doa")
    dfa.translate_to_doa("test_out.doa")

    assert set(dfa.states) == {'0', '1', '2', '3', '4', '5', '6', '1_2', '4_6', '5_6', '2_4_6', '4_5_6', 'X'}
