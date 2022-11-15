from sources.Grammars import Grammar, CockeYoungerKasami

grm = Grammar("my_grm.grm")
grm.convert_to_chomsky_normal_form(study_mode="aaaa")
grm.write_as_grm("Max_Norm.grm")
# cyk = CockeYoungerKasami(grm, convert_to_chomsky=True)

# with open("test", "r") as f:
#     for ind, line in enumerate(f.readlines()):
#         word, a = line.strip().split()
#         if ind % 100 == 0:
#             print(ind, word)
#         ans = a == "1"
#         my_ans = cyk.check_word_occurrence(word)
#         assert my_ans == ans
