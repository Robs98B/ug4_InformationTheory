def _next_checknode(packets):
    try:
        return next((i, p.pop()) for (i, p) in enumerate(packets)
                    if len(p) == 1)
    except StopIteration:
        raise ValueError('undecodable')


def _is_decoded(packets):
    return sum(map(len, packets)) == 0


def decode(received, packets):
    assert len(received) == len(packets)
    is_decoded = lambda: _is_decoded(packets)
    next_checknode = lambda: _next_checknode(packets)

    decoded = [None] * len(received)
    while not is_decoded():
        i1, i2 = next_checknode()
        decoded[i2] = received[i1]
        for (i, li) in enumerate(packets):
            try:
                li.remove(i2)
                received[i] ^= received[i1]
            except ValueError:
                continue
    return decoded


def _main(received_file, packets_file):
    received = [int(x) for l in received_file for x in l.strip().split()]
    packets = [[int(x) for x in l.strip().split()] for l in packets_file]
    decoded = decode(received, packets)
    packets_used = [i for (i, num) in enumerate(decoded) if num is not None]
    packets_unused = [i for (i, num) in enumerate(decoded) if num is None]
    decoded_msg = ''.join(chr(num) for num in decoded if num is not None)
    print 'Packets used:\t%s' % packets_used
    print 'Packets unused:\t%s' % packets_unused
    print 'Decoded string:\t"%s"' % decoded_msg


def _test():
    pass


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=2).process_args()
