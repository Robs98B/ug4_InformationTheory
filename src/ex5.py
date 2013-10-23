from __future__ import division
from collections import defaultdict
from math import log
from util import bigrams


def _main(f):
    text = ''.join(l.strip() for l in f)
    A = len(set(text))

    k_unigram = defaultdict(int)
    logprob_unigram = 0
    for (n, ai) in enumerate(text):
        p = (k_unigram[ai] + 1) / (n + A)
        assert 0 <= p <= 1, 'probabilities must be in [0,1]'
        logprob_unigram += log(p)
        k_unigram[ai] += 1
    print 'unigram: nbits < %f' % (2 - logprob_unigram)

    k_bigram = defaultdict(int)
    njs = defaultdict(int)
    logprob_bigram = 0
    for (n, (ai, aj)) in enumerate(bigrams(text)):
        kij = k_bigram[(ai, aj)]
        nj = njs[aj]
        p = (kij + 1) / (nj + A)
        assert 0 <= p <= 1, 'probabilities must be in [0,1]'
        logprob_bigram += log(p)
        k_bigram[(ai, aj)] += 1
        njs[aj] += 1
    print 'bigram:  nbits < %f' % (2 - logprob_bigram)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
