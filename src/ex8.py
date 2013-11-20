from random import random
from util import Counter


class BinarySymmetricChannel(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, seq):
        def _call(seq):
            for x in seq:
                x = int(x)
                if random() < self.f:
                    x = int(not(x))
                yield str(x)
        return list(_call(seq))


class RepetitionCode(object):
    def __init__(self, nreps):
        self.nreps = nreps

    def encode(self, seq):
        def _encode(seq):
            for x in seq:
                for _ in xrange(self.nreps):
                    yield x
        return list(_encode(seq))

    def decode(self, seq):
        def _decode(seq):
            li = list(seq)
            for i in xrange(0, len(li), self.nreps):
                chunk = li[i:i + self.nreps]
                yield Counter(chunk).most_common_element()
        return list(_decode(seq))


def _main(flip_probability):
    pass


def _test():
    message = '101'
    for flip_probability in (0.4, 0.1, 0.01):
        bsc = BinarySymmetricChannel(flip_probability)
        rc = RepetitionCode(3)
        encoded = rc.encode(message)
        received = bsc(encoded)
        decoded = rc.decode(received)
        print '***** REPETITION CODE f=%s *****' % flip_probability
        print 'message:  %s' % ''.join(message)
        print 'encoded:  %s' % ''.join(encoded)
        print 'received: %s' % ''.join(received)
        print 'decoded:  %s' % ''.join(decoded)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
