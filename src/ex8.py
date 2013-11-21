from __future__ import division
from abc import ABCMeta, abstractmethod
from numpy import array
from random import random
from util import Counter, chunks, hamming_distance


class BinarySymmetricChannel(object):
    def __init__(self, f):
        self.f = f

    def transmit(self, seq):
        def _call(seq):
            for x in seq:
                x = int(x)
                if random() < self.f:
                    x = int(not(x))
                yield x
        return list(_call(seq))


class Code(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def encode(self, seq):
        pass

    @abstractmethod
    def decode(self, seq):
        pass

    def rate(self, seq):
        return len(list(seq)) / len(self.encode(seq))

    def analyze_performance(self, channel, message_length, num_trials=100):
        errors = 0
        for _ in xrange(num_trials):
            message = [int(round(random()))
                       for _ in xrange(message_length)]
            encoded = self.encode(message)
            received = channel.transmit(encoded)
            decoded = self.decode(received)
            errors += hamming_distance(message, decoded)
        bit_error_probability = errors / (num_trials * message_length)
        return bit_error_probability, self.rate(message)


class HammingCode(Code):
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
                    error_bit = int(''.join(map(str, syndrome)), 2) - 1
                    chunk[error_bit] = int(not(chunk[error_bit]))
                decoded = HammingCode.P.dot(chunk)
                for x in decoded:
                    yield x
        return list(_decode(list(seq)))


class RepetitionCode(Code):
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


class InterleavingCode(Code):
    def __init__(self, depth):
        self._d = depth

    def encode(self, seq):
        """
        >>> ic = InterleavingCode(4)
        >>> ic.encode([1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1])
        [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        """
        def _encode(li):
            ncols = len(li) // self._d
            lim = ncols * self._d
            for chunk in zip(*chunks(li[:lim], self._d)):
                for x in chunk:
                    yield x
            for x in li[lim:]:
                yield x
        return list(_encode(list(seq)))

    def decode(self, seq):
        """
        >>> ic = InterleavingCode(4)
        >>> ic.decode([1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1])
        [1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
        """
        def _decode(li):
            ncols = len(li) // self._d
            lim = ncols * self._d
            for chunk in zip(*chunks(li[:lim], ncols)):
                for x in chunk:
                    yield x
            for x in li[lim:]:
                yield x
        return list(_decode(list(seq)))


class IRHCode(InterleavingCode, HammingCode, RepetitionCode):
    def __init__(self, nreps, depth):
        HammingCode.__init__(self)
        RepetitionCode.__init__(self, nreps)
        InterleavingCode.__init__(self, depth)

    def encode(self, seq):
        seq = RepetitionCode.encode(self, seq)
        #seq = HammingCode.encode(self, seq)
        #seq = InterleavingCode.encode(self, seq)
        return seq

    def decode(self, seq):
        #seq = InterleavingCode.decode(self, seq)
        #seq = HammingCode.decode(self, seq)
        seq = RepetitionCode.decode(self, seq)
        return seq


def _main(code_type, msg_lengths=None):
    msg_lengths = msg_lengths or [4 * x for x in (1, 10, 100, 1000, 10000)]
    code = IRHCode(3, 3)
    with open(code_type + '.csv', 'w') as f:
        f.write('# channel flip probability,'
                '# message length,'
                '# bit error probability,'
                '# rate\n')
        for flip_probability in (0.4, 0.1, 0.01, 0.001):
            bsc = BinarySymmetricChannel(flip_probability)
            for msg_length in msg_lengths:
                error, rate = code.analyze_performance(bsc, msg_length)
                f.write('%s,%s,%s,%s\n'
                        % (flip_probability, msg_length, error, rate))


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
