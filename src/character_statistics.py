#!/usr/bin/env python


from __future__ import division
from collections import defaultdict
from itertools import izip
from math import log


class Counter(defaultdict):
    def __init__(self, iterable):
        defaultdict.__init__(self, int)
        for x in iterable:
            self[x] += 1

    def total(self):
        return sum(self.itervalues())

    def to_probability_distribution(self):
        xs = self.keys()
        ps = [self[x] / self.total() for x in xs]
        return ProbabilityDistribution(ps, xs)


class ProbabilityDistribution(object):
    def __init__(self, ps, xs=None):
        assert_is_probability_distribution(ps)
        xs = xs or ('x%d' % i for i in xrange(len(ps)))
        self._d = dict(izip(xs, ps))

    def __call__(self, x):
        return self._d[x]

    def entropy(self):
        return _entropy(self._d.values())


def assert_is_probability_distribution(ps):
    assert '1.000' == '%.3f' % sum(ps), 'probabilities must sum to 1'
    assert all(0 <= p for p in ps), 'probabilities must be >=0'
    assert all(1 >= p for p in ps), 'probabilities must be <=1'


def _entropy(ps, base=2):
    """
    >>> print '%.3f' % _entropy([0.0, 1.0])
    0.000
    >>> print '%.3f' % _entropy([0.5, 0.5])
    1.000
    >>> print '%.3f' % _entropy([0.2, 0.8])
    0.722
    >>> print '%.3f' % _entropy([0.8, 0.2])
    0.722
    >>> print '%.3f' % _entropy([0.5, 0.25, 0.125, 0.125])
    1.750
    """
    return sum(-p * log(p, base) for p in ps if p != 0)


def _ex1(text):
    """
    >>> _ex1('aaaaa')
    H(Xn) = 0.000
    >>> _ex1('aabb')
    H(Xn) = 1.000
    >>> _ex1('aaaab')
    H(Xn) = 0.722
    >>> _ex1('abbbb')
    H(Xn) = 0.722
    >>> _ex1('aaaabbcd')
    H(Xn) = 1.750
    """
    unigram_pd = Counter(text).to_probability_distribution()
    print 'H(Xn) = %.3f' % unigram_pd.entropy()


def _ex2(text):
    bigram_pd = Counter(izip(text, text[1:])).to_probability_distribution()
    unigram_pd = Counter(text).to_probability_distribution()
    print 'H(Xn, Xn+1) = %.3f' % bigram_pd.entropy()
    print 'H(Xn+1 | Xn) = %.3f' % (bigram_pd.entropy() - unigram_pd.entropy())


def _main(f):
    text = ''.join(l.strip() for l in f)
    _ex1(text)
    _ex2(text)


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    import optparse
    import sys

    parser = optparse.OptionParser(usage='usage: %prog [options] input')
    parser.add_option('-t', '--run-tests', help='run tests and exit',
                      action='store_true', dest='run_tests')
    options, args = parser.parse_args()

    if options.run_tests:
        _test()
        sys.exit()

    try:
        with open(args[0]) as f:
            _main(f)
    except IndexError:
        sys.exit('need to specify input file\n%s' % parser.get_usage())
