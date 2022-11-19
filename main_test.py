import sources.Grammars as Grm

my_grm = Grm.Grammar("test_cyk_by_pytest/grm_texts/grm_base_check.grm")
# my_grm.convert_to_chomsky_normal_form()
# my_grm.write_as_grm("test_cyk_by_pytest/grm_texts/grm_base_output_check.grm")
# print("".join(my_grm.generate_word()))

earley = Grm.Earley(my_grm)
print(earley.check_word_occurrence('()'))
