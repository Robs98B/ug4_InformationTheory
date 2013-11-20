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

    def analyze_performance(self, channel, message_length, num_trials=10):
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


class RepetitionHammingCode(HammingCode, RepetitionCode):
    def __init__(self, nreps):
        HammingCode.__init__(self)
        RepetitionCode.__init__(self, nreps)

    def encode(self, seq):
        return RepetitionCode.encode(self, HammingCode.encode(self, seq))

    def decode(self, seq):
        return HammingCode.decode(self, RepetitionCode.decode(self, seq))


def _main(code_type, max_message_length=10000):
    code_type = code_type.lower()
    with open(code_type + '_code_performance.csv', 'wa') as f:
        f.write('# channel flip probability,'
                '# message length,'
                '# bit error probability,'
                '# rate\n')
        for flip_probability in (0.4, 0.1, 0.01):
            bsc = BinarySymmetricChannel(flip_probability)
            if code_type == 'hamming':
                code = HammingCode()
            elif code_type.startswith('repetition'):
                code = RepetitionCode(int(code_type.split('-')[1]))
            elif code_type.startswith('hr'):
                code = RepetitionHammingCode(int(code_type.split('-')[1]))
            for message_length in xrange(4, max_message_length, 4):
                error, rate = code.analyze_performance(bsc, message_length)
                f.write('%s,%s,%s,%s\n'
                        % (flip_probability, message_length, error, rate))


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
