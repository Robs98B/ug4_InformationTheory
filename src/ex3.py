from util import Counter, bigrams


def _main(f):
    """
    >>> _main('abaab')
    unigram: nbits < 6.854753
    bigram:  nbits < 5.204141
    """
    text = ''.join(l.strip() for l in f)
    p_unigram = Counter(text).to_probability_distribution()
    unigram_textprob = p_unigram.logprob(text)
    print 'unigram: nbits < %f' % (2 - unigram_textprob)

    text_bigrams = list(bigrams(text))
    p_bigram = Counter(text_bigrams).to_probability_distribution()
    bigram_textprob = p_bigram.conditional_logprob(p_unigram, text_bigrams)
    print 'bigram:  nbits < %f' % (2 - bigram_textprob)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
