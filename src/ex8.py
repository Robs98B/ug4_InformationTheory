from numpy import array
from random import random
from util import Counter, chunks


class BinarySymmetricChannel(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, seq):
        def _call(seq):
            for x in seq:
                x = int(x)
                if random() < self.f:
                    x = int(not(x))
                yield x
        return list(_call(seq))


class HammingCode(object):
    G = array([[1, 1, 0, 1],
               [1, 0, 1, 1],
               [1, 0, 0, 0],
               [0, 1, 1, 1],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
    H = array([[1, 0, 1, 0, 1, 0, 1],
               [0, 1, 1, 0, 0, 1, 1],
               [0, 0, 0, 1, 1, 1, 1]])
    P = array([[0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 1]])

    def encode(self, seq):
        """
        >>> hc = HammingCode()
        >>> hc.encode([1, 0, 1, 1])
        [0, 1, 1, 0, 0, 1, 1]
        """
        def _encode(li):
            for chunk in map(array, chunks(li, 4)):
                output = HammingCode.G.dot(chunk) % 2
                for x in output:
                    yield x
        return list(_encode(list(seq)))

    def decode(self, seq):
        """
        >>> hc = HammingCode()
        >>> hc.decode([0, 1, 1, 0, 0, 1, 1]) == [1, 0, 1, 1]  # no errors
        True
        >>> hc.decode([0, 1, 1, 1, 0, 1, 1]) == [1, 0, 1, 1]  # one error
        True
        >>> hc.decode([0, 1, 1, 1, 0, 0, 1]) == [1, 0, 1, 1]  # two errors
        False
        """
        def _decode(li):
            for chunk in map(array, chunks(li, 7)):
                syndrome = HammingCode.H.dot(chunk) % 2
                if not all(x == 0 for x in syndrome):
                    error_bit = int(''.join(map(str, syndrome)), 2)
                    chunk[error_bit] = int(not(chunk[error_bit]))
                decoded = HammingCode.P.dot(chunk)
                for x in decoded:
                    yield x
        return list(_decode(list(seq)))


class RepetitionCode(object):
    def __init__(self, nreps):
        self.nreps = nreps

    def encode(self, seq):
        """
        >>> rc = RepetitionCode(3)
        >>> rc.encode([1, 0, 1])
        [1, 1, 1, 0, 0, 0, 1, 1, 1]
        """
        def _encode(seq):
            for x in seq:
                for _ in xrange(self.nreps):
                    yield x
        return list(_encode(seq))

    def decode(self, seq):
        """
        >>> rc = RepetitionCode(3)
        >>> rc.decode([1, 1, 1, 0, 0, 0, 1, 1, 1])  # no errors
        [1, 0, 1]
        >>> rc.decode([1, 1, 0, 0, 0, 1, 1, 1, 0]) == [1, 0,1]  # one error
        True
        >>> rc.decode([1, 0, 0, 0, 0, 1, 1, 1, 0]) == [1, 0, 1]  # two errors
        False
        """
        def _decode(seq):
            for chunk in chunks(seq, self.nreps):
                yield Counter(chunk).most_common_element()
        return list(_decode(seq))


class RepetitionHammingCode(HammingCode, RepetitionCode):
    def __init__(self, nreps):
        HammingCode.__init__(self)
        RepetitionCode.__init__(self, nreps)

    def encode(self, seq):
        return RepetitionCode.encode(self, HammingCode.encode(self, seq))

    def decode(self, seq):
        return HammingCode.decode(self, RepetitionCode.decode(self, seq))


def _main(flip_probability, message_length):
    message = [int(round(random())) for _ in xrange(message_length)]
    code = RepetitionHammingCode(nreps=3)
    encoded = code.encode(message)
    received = encoded
    decoded = code.decode(received)
    print 'message:  %s' % ''.join(map(str, message))
    print 'encoded:  %s' % ''.join(map(str, encoded))
    print 'received: %s' % ''.join(map(str, received))
    print 'decoded:  %s' % ''.join(map(str, decoded))


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=2).process_args()
