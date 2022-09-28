import pytest

from sources.DFA import NFA


def test_alphabet_good():
    m1 = NFA.NFA(alphabet="abcd", regex="abc bd + d * ac ^+ abc * +")

    m2 = NFA.NFA(regex="bc be + d * fc ^+ ebc * +")
    assert set(m2.alphabet) == {'b', 'c', 'e', 'd', 'f'}

    m3 = NFA.NFA(alphabet="abcd", doa_file="test_by_pytest/doa_texts/doa_1.doa")

    m4 = NFA.NFA(doa_file="test_by_pytest/doa_texts/doa_1.doa")
    assert set(m4.alphabet) == {'a', 'b'}


def test_alphabet_error():
    with pytest.raises(Exception):
        m1 = NFA.NFA(alphabet="abcd", regex="abc bd + d * aec ^+ abc * +")

    with pytest.raises(Exception):
        m2 = NFA.NFA(alphabet="bcd", doa_file="test_by_pytest/doa_texts/doa_1.doa")