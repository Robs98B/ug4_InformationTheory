from util import Counter


def _main(f):
    """
    >>> _main('aaaaa')
    H(Xn) = 0.000

    >>> _main('aabb')
    H(Xn) = 1.000

    >>> _main('aaaab')
    H(Xn) = 0.722

    >>> _main('abbbb')
    H(Xn) = 0.722

    >>> _main('aaaabbcd')
    H(Xn) = 1.750
    """
    text = ''.join(l.strip() for l in f)
    unigram_pd = Counter(text).to_probability_distribution()
    print 'H(Xn) = %.3f' % unigram_pd.entropy()


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
