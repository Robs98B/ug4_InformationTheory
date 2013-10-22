#!/usr/bin/env python


from itertools import izip


def xor(char1, num):
    return chr(ord(char1) ^ num)


def _ex6():
    message = 'nutritious snacks'
    nums = [59, 6, 17, 0, 83, 84, 26, 90, 64, 70, 25, 66, 86, 82, 90, 95, 75]
    print ''.join(xor(char, num) for (char, num) in izip(message, nums))


def _main():
    _ex6()


if __name__ == '__main__':
    _main()
