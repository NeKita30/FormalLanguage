from sources.Machines import NFA


def test_trans_2_doa():
    m = NFA.NFA(regex="ab ^+ aab ^+ *")
    m.translate_to_doa("borrowing/popyt.doa")
    m1 = NFA.NFA(regex="b ^* b ^* a * b ^* * a * b ^* * ^* +")
    m1.translate_to_doa("borrowing/popyt2")


def test_trans_from_doa():
    m = NFA.NFA(doa_file="test_by_pytest/doa_texts/doa_1.doa")
    m.translate_to_doa("test_by_pytest/doa_texts/doa_1_result")

    m1 = NFA.NFA(doa_file="test_by_pytest/doa_texts/doa_2.doa")
    m1.translate_to_doa("test_by_pytest/doa_texts/doa_2_result")
