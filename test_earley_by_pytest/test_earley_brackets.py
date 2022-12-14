from sources.Grammars import Grammar, Earley


def test_earley_brackets():
    def generate_words(size, cnt_round_open=0, cnt_round_close=0,
                       cnt_square_open=0, cnt_square_close=0,
                       cnt_brace_open=0, cnt_brace_close=0,
                       cnt_less_open=0, cnt_more_close=0,
                       w=""):
        if cnt_round_open + cnt_square_open + cnt_brace_open + cnt_less_open + \
                + cnt_round_close + cnt_square_close + cnt_brace_close + cnt_more_close == 2 * size:
            yield w
        if cnt_round_open + cnt_square_open + cnt_brace_open + cnt_less_open < size:
            for next_word in generate_words(size, cnt_round_open + 1, cnt_round_close,
                                            cnt_square_open, cnt_square_close,
                                            cnt_brace_open, cnt_brace_close,
                                            cnt_less_open, cnt_more_close,
                                            w + '('):
                yield next_word
            for next_word in generate_words(size, cnt_round_open, cnt_round_close,
                                            cnt_square_open + 1, cnt_square_close,
                                            cnt_brace_open, cnt_brace_close,
                                            cnt_less_open, cnt_more_close,
                                            w + '['):
                yield next_word
            for next_word in generate_words(size, cnt_round_open, cnt_round_close,
                                            cnt_square_open, cnt_square_close,
                                            cnt_brace_open + 1, cnt_brace_close,
                                            cnt_less_open, cnt_more_close,
                                            w + '{'):
                yield next_word
            for next_word in generate_words(size, cnt_round_open, cnt_round_close,
                                            cnt_square_open, cnt_square_close,
                                            cnt_brace_open, cnt_brace_close,
                                            cnt_less_open + 1, cnt_more_close,
                                            w + '<'):
                yield next_word
        if cnt_round_open > cnt_round_close:
            for next_word in generate_words(size, cnt_round_open, cnt_round_close + 1,
                                            cnt_square_open, cnt_square_close,
                                            cnt_brace_open, cnt_brace_close,
                                            cnt_less_open, cnt_more_close,
                                            w + ')'):
                yield next_word
        if cnt_square_open > cnt_square_close:
            for next_word in generate_words(size, cnt_round_open, cnt_round_close,
                                            cnt_square_open, cnt_square_close + 1,
                                            cnt_brace_open, cnt_brace_close,
                                            cnt_less_open, cnt_more_close,
                                            w + ']'):
                yield next_word
        if cnt_brace_open > cnt_brace_close:
            for next_word in generate_words(size, cnt_round_open, cnt_round_close,
                                            cnt_square_open, cnt_square_close,
                                            cnt_brace_open, cnt_brace_close + 1,
                                            cnt_less_open, cnt_more_close,
                                            w + '}'):
                yield next_word
        if cnt_less_open > cnt_more_close:
            for next_word in generate_words(size, cnt_round_open, cnt_round_close,
                                            cnt_square_open, cnt_square_close,
                                            cnt_brace_open, cnt_brace_close,
                                            cnt_less_open, cnt_more_close + 1,
                                            w + '>'):
                yield next_word

    def test_brackets(w):
        stck = list()
        for c in w:
            if c in {'(', '[', '{', '<'}:
                stck.append(c)
            else:
                if c == ')' and stck[-1] == '(':
                    stck.pop()
                elif c == '}' and stck[-1] == '{':
                    stck.pop()
                elif c == ']' and stck[-1] == '[':
                    stck.pop()
                elif c == '>' and stck[-1] == '<':
                    stck.pop()
        return not stck

    grm = Grammar('test_earley_by_pytest/grm_brackets.grm')
    earley = Earley(grm)
    for word in generate_words(4):
        assert earley.check_word_occurrence(word) == test_brackets(word)
