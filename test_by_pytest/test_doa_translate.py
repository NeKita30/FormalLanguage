from sources.Machines import NFA
import os


def test_trans_2_doa():
    m = NFA.NFA(regex="ab ^+ aab ^+ *")
    m.translate_to_doa("borrowing/popyt.doa")
    m1 = NFA.NFA(regex="b ^* b ^* a * b ^* * a * b ^* * ^* +")
    m1.translate_to_doa("borrowing/popyt2")
    os.remove('borrowing/popyt.doa')
    os.remove('borrowing/popyt2.doa')


def test_trans_from_doa():
    m = NFA.NFA(doa_file="test_by_pytest/doa_texts/doa_1.doa")
    m.translate_to_doa("test_by_pytest/doa_texts/doa_1_result")
    with open("test_by_pytest/doa_texts/doa_1.doa", "r") as in_f:
        with open("test_by_pytest/doa_texts/doa_1_result.doa", 'r') as out_file:
            for in_line, out_line in zip(in_f.readlines(), out_file.readlines()):
                assert in_line == out_line

    m1 = NFA.NFA(doa_file="test_by_pytest/doa_texts/doa_2.doa")
    m1.translate_to_doa("test_by_pytest/doa_texts/doa_2_result")
    with open("test_by_pytest/doa_texts/doa_2.doa", "r") as in_f:
        with open("test_by_pytest/doa_texts/doa_2_result.doa", 'r') as out_file:
            for in_line, out_line in zip(in_f.readlines(), out_file.readlines()):
                assert in_line == out_line
    os.remove("test_by_pytest/doa_texts/doa_1_result.doa")
    os.remove("test_by_pytest/doa_texts/doa_2_result.doa")