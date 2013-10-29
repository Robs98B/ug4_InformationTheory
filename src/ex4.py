from math import ceil
from util import Counter, ProbabilityDistribution, log2


def round_pow2(num, n=8):
    pow2 = 2 ** n
    return ceil(pow2 * num) / pow2


def approximate_probability_distribution(p, nbits):
    """
    >>> p = Counter('abaab').to_probability_distribution()
    >>> q = approximate_probability_distribution(p, 8)
    >>> q('a') == 154.0 / 257 and q('b') == 103.0 / 257
    True
    """
    q = [round_pow2(pi, nbits) for pi in p.probabilities()]
    return ProbabilityDistribution([qi / sum(q) for qi in q], p.symbols())


def _main(f):
    """
    >>> _main('abaab')
    header:  nbits = 8
    message: nbits < 6.854762
    """
    header_bits_per_symbol = 8

    text = ''.join(l.strip() for l in f)
    nsymbols = len(set(text))
    print 'header:  nbits = %d' % ((nsymbols - 1) * header_bits_per_symbol)

    p = Counter(text).to_probability_distribution()
    q = approximate_probability_distribution(p, header_bits_per_symbol)

    logprob_q = sum(log2(q(x)) for x in text)
    print 'message: nbits < %f' % (2 - logprob_q)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
