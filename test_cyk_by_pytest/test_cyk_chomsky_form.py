import sources.Grammars as Grm


def test_cyk_chomsky_form_ungenerating():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_ungenerating.grm")
    grm._Grammar__delete_no_generating_nonterminals()
    assert set(grm.nonterminals) == {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
    assert set(grm.rules['A'].rights) == {('A', 'B'), ('C', 'a')}
    assert set(grm.rules['G'].rights) == {('a', 'E', 'F'), ('D', 'E')}
    assert set(grm.rules['F'].rights) == {('F', 'a', 'G'), ('D', 'G')}


def test_cyk_chomsky_form_unreached():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_unreachable.grm")
    grm._Grammar__delete_unreachable_nonterminals()
    assert set(grm.nonterminals) == {'A', 'B', 'D', 'E'}

    grm.nonterminals = ['B', 'D']
    grm._Grammar__delete_unreachable_nonterminals()
    assert grm.nonterminals == list()
    assert grm.rules == dict()


def test_cyk_search_new_nonterminal():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_base_check.grm")
    x = Grm.Grammar._Grammar__search_new_nonterminal(grm.nonterminals+grm.alphabet, end="_a")
    assert x == "A_a"
    grm.nonterminals.append(x)
    x = Grm.Grammar._Grammar__search_new_nonterminal(grm.nonterminals+grm.alphabet, end="_a")
    assert x == "B_a"
    grm.nonterminals = [chr(i) for i in range(65, 91)]
    x = Grm.Grammar._Grammar__search_new_nonterminal(grm.nonterminals+grm.alphabet)
    assert x == "AA"


def test_cyk_chomsky_form_mixed_transitions():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_mixed.grm")
    grm._Grammar__delete_mixed_transitions()
    assert set(grm.nonterminals) == {'A', 'A_b', 'B', 'C', 'D', 'E', 'F', 'G', 'A_a', 'B_b'}
    assert ('C', 'A_a', 'A') in grm.rules['A'].rights
    assert ('A_a', 'D', 'F', 'B_b', 'E') in grm.rules['B'].rights
    assert ('A_a', 'E', 'F', 'B_b', 'A_a', 'D') in grm.rules['G'].rights
    assert ('a',) in grm.rules['B'].rights
    assert ('A_a', 'A_a') in grm.rules['E'].rights


def test_cyk_chomsky_form_long_transitions():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_long.grm")
    grm._Grammar__delete_long_transitions()
    assert set(grm.nonterminals) == {'A', 'B', 'C', 'D', 'E', 'F',
                                     'A_1', 'A_2', 'A_3', 'A_4', 'A_5',
                                     'A_6', 'A_7'}
    assert set(grm.rules['A'].rights) == {('A', 'B'), ('C', 'A'), ('ε',)}
    assert set(grm.rules['B'].rights) == {('B', 'A_1')}
    assert set(grm.rules['A_1'].rights) == {('D', 'A_2')}
    assert set(grm.rules['A_2'].rights) == {('C', 'D')}
    assert set(grm.rules['C'].rights) == {('B', 'A_3'), ('C', 'A_4'), ('E', 'A_5')}
    assert set(grm.rules['F'].rights) == {('A',), ('ε',), ('E',)}


def test_cyk_chomsky_form_eps_transition():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_eps.grm")
    grm._Grammar__delete_eps_transitions()
    assert set(grm.nonterminals) == {'A_0', 'A', 'B', 'C', 'D', 'E', 'F'}
    assert set(grm.rules['A'].rights) == {('B', 'C'), ('C', 'E'), ('B',), ('C',), ('E',)}
    assert set(grm.rules['B'].rights) == {('a',), ('D',)}
    assert set(grm.rules['C'].rights) == {('F',), ('E',)}
    assert set(grm.rules['D'].rights) == {('A', 'B'), ('b',), ('B',)}
    assert set(grm.rules['E'].rights) == {('F',)}
    assert grm.rules['F'].rights == [('b',)]
    assert 'G' not in grm.rules


def test_cyk_chomsky_form_unit_transition():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_unit_trans.grm")
    grm._Grammar__delete_unit_transitions()
    assert set(grm.rules['A'].rights) == {('B', 'D'), ('a',), ('C', 'D'), ('b',), ('D', 'E')}
    assert set(grm.rules['B'].rights) == {('D', 'E'), ('a',), ('C', 'D'), ('b',)}
    assert set(grm.rules['C'].rights) == {('D', 'E'), ('a',)}


def test_cyk_chomsky_form_complete():
    grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_complete.grm")
    grm.convert_to_chomsky_normal_form()
    assert set(grm.nonterminals) == {'A', 'A_0', 'A_1', 'A_2', 'A_a',
                                     'A_b', 'B', 'C', 'D', 'E'}
    assert set(grm.rules['A_0'].rights) == {('A', 'A_1'), ('a',), ('ε',),  ('A_b', 'A_2')}
    assert set(grm.rules['A'].rights) == {('A', 'A_1'), ('a',), ('A_b', 'A_2')}
    assert set(grm.rules['A_1'].rights) == {('A_b', 'A_2')}
    assert set(grm.rules['A_2'].rights) == {('B', 'A_a'), ('a',)}
    assert set(grm.rules['A_a'].rights) == {('a',)}
    assert set(grm.rules['A_b'].rights) == {('b',)}
    assert set(grm.rules['B'].rights) == {('C', 'D'), ('b',), ('D', 'E'), ('a',), ('b',)}
    assert set(grm.rules['C'].rights) == {('D', 'E'), ('a',), ('b',)}
    assert grm.rules['D'].rights == [('a',)]
    assert grm.rules['E'].rights == [('b',)]
