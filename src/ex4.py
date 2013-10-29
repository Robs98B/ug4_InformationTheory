from math import ceil
from util import Counter, ProbabilityDistribution, bigrams


def round_pow2(num, n=8):
    pow2 = 2 ** n
    return ceil(pow2 * num) / pow2


def approximate(p, nbits):
    """
    >>> p = Counter('abaab').to_probability_distribution()
    >>> q = approximate(p, 8)
    >>> q('a') == 154.0 / 257 and q('b') == 103.0 / 257
    True
    """
    q = [round_pow2(pi, nbits) for pi in p.probabilities()]
    return ProbabilityDistribution([qi / sum(q) for qi in q], p.symbols())


def _main(f):
    """
    >>> _main('abaab')
    unigram header:  nbits = 8
    unigram message: nbits < 6.854762
    bigram header:  nbits = 24
    bigram message: nbits < 5.203200

    >>> _main('bccccba')
    unigram header:  nbits = 16
    unigram message: nbits < 11.651541
    bigram header:  nbits = 64
    bigram message: nbits < 7.706959
    """
    header_bits_per_symbol = 8

    text = ''.join(l.strip() for l in f)
    nsymbols = len(set(text))
    unigram_header_size = (nsymbols - 1) * header_bits_per_symbol
    print 'unigram header:  nbits = %d' % unigram_header_size
    p_unigram = Counter(text).to_probability_distribution()
    q_unigram = approximate(p_unigram, header_bits_per_symbol)
    unigram_textprob = q_unigram.logprob(text)
    print 'unigram message: nbits < %f' % (2 - unigram_textprob)

    text_bigrams = bigrams(text)
    nsymbols = len(set(text)) ** 2
    bigram_header_size = (nsymbols - 1) * header_bits_per_symbol
    print 'bigram header:  nbits = %d' % bigram_header_size
    p_bigram = Counter(text_bigrams).to_probability_distribution()
    q_bigram = approximate(p_bigram, header_bits_per_symbol)
    bigram_textprob = q_bigram.conditional_logprob(q_unigram, text_bigrams)
    print 'bigram message: nbits < %f' % (2 - bigram_textprob)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
