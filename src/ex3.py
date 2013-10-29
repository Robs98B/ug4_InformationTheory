from util import Counter, bigrams, log2


def _main(f):
    text = ''.join(l.strip() for l in f)
    p_unigram = Counter(text).to_probability_distribution()
    logprob_unigram = sum(log2(p_unigram(x)) for x in text)
    print 'unigram: nbits < %f' % (2 - logprob_unigram)

    text_bigrams = list(bigrams(text))
    p_bigram = Counter(text_bigrams).to_probability_distribution()
    logprob_bigram = log2(p_unigram(text[0]))
    for (xm, xn) in text_bigrams:
        logprob_bigram += log2(p_bigram((xm, xn))) - log2(p_unigram(xm))
    print 'bigram:  nbits < %f' % (2 - logprob_bigram)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
