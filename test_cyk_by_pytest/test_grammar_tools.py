from sources.Grammars import Grammar


def test_cyk_trans_from_grm():
    grm = Grammar("test_cyk_by_pytest/grm_texts/grm_base_check.grm")
    grm.write_as_grm("test_cyk_by_pytest/grm_texts/grm_base_output_check.grm")


def test_generate_word():
    def check_bracket_balance(word_to_check):
        balance = 0
        for a in word_to_check:
            if a in {'(', '{', '['}:
                balance += 1
            elif a in {')', '}', ']'}:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    grm = Grammar("test_cyk_by_pytest/grm_texts/grm_bracket_words.grm")
    for i in range(5):
        word = grm.generate_word(limit=10)
        assert check_bracket_balance(word)


def test_chomsky_form_check():
    grm_1 = Grammar("test_cyk_by_pytest/grm_texts/grm_bracket_words.grm")
    assert not grm_1.check_chomsky_form()

    grm_2 = Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_eps.grm")
    assert not grm_2.check_chomsky_form()

    grm_3 = Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_long.grm")
    assert not grm_3.check_chomsky_form()

    grm_4 = Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_unit_trans.grm")
    assert not grm_4.check_chomsky_form()

    grm_5 = Grammar("test_cyk_by_pytest/grm_texts/grm_chomsky_form_check.grm")
    assert not grm_5.check_chomsky_form()
