from math import ceil, log
from util import Counter, ProbabilityDistribution


def round_pow2(num, n=8):
    pow2 = 2 ** n
    return ceil(pow2 * num) / pow2


def _main(f):
    header_bits_per_symbol = 8

    text = ''.join(l.strip() for l in f)
    nsymbols = len(set(text))
    print 'header: nbits = %d' % ((nsymbols - 1) * header_bits_per_symbol)

    p = Counter(text).to_probability_distribution()
    q = [round_pow2(pi, header_bits_per_symbol) for pi in p.probabilities]
    q = [qi / sum(q) for qi in q]
    q = ProbabilityDistribution(q, p.symbols)

    logprob_q = sum(log(q(x)) for x in text)
    print 'message: nbits < %f' % (2 - logprob_q)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
