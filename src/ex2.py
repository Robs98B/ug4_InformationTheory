from util import Counter, bigrams


def _main(f):
    """
    >>> _main('aa')
    H(Xn, Xn+1) = 0.000
    H(Xn+1 | Xn) = 0.000

    >>> _main('ab')
    H(Xn, Xn+1) = 0.000
    H(Xn+1 | Xn) = -1.000

    >>> _main('abbabaab')
    H(Xn, Xn+1) = 1.842
    H(Xn+1 | Xn) = 0.842

    >>> _main('abcacbbca')
    H(Xn, Xn+1) = 2.500
    H(Xn+1 | Xn) = 0.915

    >>> _main('aaaaaabcac')
    H(Xn, Xn+1) = 1.880
    H(Xn+1 | Xn) = 0.723
    """
    text = ''.join(l.strip() for l in f)
    bigram_pd = Counter(bigrams(text)).to_probability_distribution()
    unigram_pd = Counter(text).to_probability_distribution()
    Hx = unigram_pd.entropy()
    Hxy = bigram_pd.entropy()
    print 'H(Xn, Xn+1) = %.3f' % Hxy
    print 'H(Xn+1 | Xn) = %.3f' % (Hxy - Hx)


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
