from util import Counter, bigrams


def _main(f):
    text = ''.join(l.strip() for l in f)
    bigram_pd = Counter(bigrams(text)).to_probability_distribution()
    unigram_pd = Counter(text).to_probability_distribution()
    print 'H(Xn, Xn+1) = %.3f' % bigram_pd.entropy()
    print 'H(Xn+1 | Xn) = %.3f' % (bigram_pd.entropy() - unigram_pd.entropy())


if __name__ == '__main__':
    from util import DefaultOptionParser
    from sys import modules
    DefaultOptionParser(caller=modules[__name__], npositional=1).process_args()
