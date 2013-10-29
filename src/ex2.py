from util import Counter, bigrams


def _main(f):
    text = ''.join(l.strip() for l in f)
    bigram_pd = Counter(bigrams(text)).to_probability_distribution()
    unigram_pd = Counter(text).to_probability_distribution()
    Hx = unigram_pd.entropy()
    Hxy = bigram_pd.entropy()
    print 'H(Xn, Xn+1) = %.3f' % Hxy
    print 'H(Xn+1 | Xn) = %.3f' % (Hxy - Hx)


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
