from itertools import izip


def xor(char1, num):
    return chr(ord(char1) ^ num)


def _main():
    message = 'nutritious snacks'
    nums = [59, 6, 17, 0, 83, 84, 26, 90, 64, 70, 25, 66, 86, 82, 90, 95, 75]
    print ''.join(xor(char, num) for (char, num) in izip(message, nums))


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=0).process_args()
