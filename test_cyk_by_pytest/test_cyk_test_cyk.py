from sources.Grammars import Grammar, CockeYoungerKasami


def test_cyk_test():
    def generate_words(size, cnt_open=0, cnt_close=0, word=""):
        if cnt_open + cnt_close == 2 * size:
            yield word
        if cnt_open < size:
            for next_word in generate_words(size, cnt_open+1, cnt_close, word+'('):
                yield next_word
        if cnt_open > cnt_close:
            for next_word in generate_words(size, cnt_open, cnt_close + 1, word+')'):
                yield next_word

    grm = Grammar("test_cyk_by_pytest/grm_texts/grm_cky.grm")

    cyk = CockeYoungerKasami(grm)
    assert cyk.check_word_occurrence("")
    for word_in_langauge in generate_words(5):
        assert cyk.check_word_occurrence(word_in_langauge)
