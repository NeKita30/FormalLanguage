from sources.Grammars import Grammar
import pytest
from sources.Grammars.errors import TranslateGrammarError


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

    grm_6 = Grammar("test_cyk_by_pytest/grm_texts/grm_not_in_chomsky.grm")
    assert not grm_6.check_chomsky_form()

    grm_6.convert_to_chomsky_normal_form()
    assert grm_6.check_chomsky_form()


def test_chomsky_study_mode():
    grm = Grammar("test_cyk_by_pytest/grm_texts/grm_not_in_chomsky.grm")
    grm.convert_to_chomsky_normal_form(study_mode="test_cyk_by_pytest/grm_texts/grm_convert_study_mode")


def test_grm_file_reading_errors():
    with pytest.raises(TranslateGrammarError) as excinfo:
        grm = Grammar("test_cyk_by_pytest/grm_texts/grm_wrong_format.txt")
    file_name = "test_cyk_by_pytest/grm_texts/grm_wrong_format.txt"
    assert str(excinfo.value) == f"Wrong \"{file_name}\" file name - should end with .grm"

    with pytest.raises(TranslateGrammarError) as excinfo:
        grm = Grammar("test_cyk_by_pytest/grm_texts/grm_wrong_nonterm_line.grm")
    assert str(excinfo.value) == f"""Wrong nonterminal list line - should be:
Nonterm.: A B A_1 C D\\B
but get:
Nonterm: A B C A_c A_1 A_0"""

    with pytest.raises(TranslateGrammarError) as excinfo:
        grm = Grammar("test_cyk_by_pytest/grm_texts/grm_wrong_alphabet_line.grm")
    assert str(excinfo.value) == f"""Wrong alphabet line - should be:
Alphabet: a b c a_1 a_2 
but get:
Alphabit: a b c"""

    with pytest.raises(TranslateGrammarError) as excinfo:
        grm = Grammar("test_cyk_by_pytest/grm_texts/grm_non_alphabet_symbol.grm")
    assert str(excinfo.value) == f"""Unknown symbol - \"x\" - in transition x"""
