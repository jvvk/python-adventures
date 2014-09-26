__author__ = 'twisa'

from mrjob.job import MRJob

QUERY = "ant"

def neighbours(words):
    setwords = set(words)
    nbrs = {}
    for w in words:
        nbrs[w] = setwords - set(w)
    return nbrs

class MRCoocPairs(MRJob):
    def mapper(self, _, line):
        words = line.split(" ")
        nbrs = neighbours(words)
        for w in words:
            if w == QUERY:
                for u in nbrs[w]:
                    yield ((w, u), 1)

    def reducer(self, key, values):
        yield key, sum(values)


class MRCoocStripes(MRJob):
    def mapper(self, _, line):
        words = line.split(" ")
        nbrs = neighbours(words)
        for w in words:
            if w == QUERY:
                h = {}
                for u in nbrs[w]:
                    h.setdefault(u, 0)
                    h[u] += 1
                yield w, h

    def reducer(self, key, values):
        hf = {}
        for h in values:
            for k, v in h.items():
                hf.setdefault(k, 0)
                hf[k] += v
        yield key, hf


if __name__ == '__main__':
    MRCoocStripes.run()