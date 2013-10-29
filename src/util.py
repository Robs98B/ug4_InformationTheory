from __future__ import division
from collections import defaultdict
from doctest import testmod
from itertools import izip
from math import log
from optparse import OptionParser
from sys import exit, stderr


class DefaultOptionParser(OptionParser):
    def __init__(self, caller, npositional=0):
        self._caller = caller
        self._npositional = npositional
        usage = ('usage: %prog [options] '
                 + ' '.join('input%d' % i for i in xrange(npositional)))
        OptionParser.__init__(self, usage=usage)
        self.add_option('-t', '--run-tests', help='run tests and exit',
                        action='store_true', dest='run_tests')

    def _warning(self, msg):
        print >> stderr, '[%s - warning] %s' % (self._caller.__file__, msg)

    def _fatal(self, msg):
        exit(msg)

    def _delegate_opts(self):
        if self.opts.run_tests:
            failure_count, test_count = testmod(self._caller)
            if test_count == 0:
                self._warning('no doc-tests implemented: no tests were run')
            exit(failure_count > 0)

    def _validate_args(self):
        if len(self.args) < self._npositional:
            self._fatal('need to specify %d input file%s (got %d)\n%s'
                        % (self._npositional,
                           's' if self._npositional > 1 else '',
                           len(self.args),
                           self.get_usage()))
        if len(self.args) > self._npositional:
            self._warning('unused arguments: %s'
                          % ', '.join(self.args[self._npositional:]))

    def _delegate_args(self):
        inputs = map(open, self.args[:self._npositional])
        try:
            self._caller._main(*inputs)
        finally:
            map(lambda f: f.close(), inputs)

    def process_args(self):
        self.opts, self.args = self.parse_args()
        self._delegate_opts()
        self._validate_args()
        self._delegate_args()


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
        self._symbols = xs
        self._probabilities = ps
        self._d = dict(izip(xs, ps))

    def probabilities(self):
        return self._probabilities

    def symbols(self):
        return self._symbols

    def __repr__(self):
        ps = sorted(self._d.iteritems())
        return ('ProbabilityDistribution[%s]'
                % (', '.join('p(%s)=%f' % t for t in ps)))

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


def bigrams(text):
    return izip(text, text[1:])


if __name__ == '__main__':
    import doctest
    doctest.testmod()
