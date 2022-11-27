import sources.Grammars as Grm

my_grm = Grm.Grammar("Max_grammar.grm")
# my_grm.convert_to_chomsky_normal_form()
# my_grm.write_as_grm("test_cyk_by_pytest/grm_texts/grm_base_output_check.grm")
# print("".join(my_grm.generate_word()))

earley = Grm.Earley(my_grm)
with open('test', 'r') as f:
    for i, line in enumerate(f.readlines()):
        word, ans = line.strip().split()
        ans = (ans == '1')
        my_ans = earley.check_word_occurrence(word)
        assert my_ans == ans
