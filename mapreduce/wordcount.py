__author__ = 'twisa'

from mrjob.job import MRJob

class MRWordCount1(MRJob):

    def mapper(self, _, line):
        words = line.split(" ")
        for w in words:
            yield w, 1

    def reducer(self, key, values):
        yield key, sum(values)


class MRWordCount2(MRJob):

    def mapper(self, _, line):
        wordmap = {}
        words = line.split(" ")
        for w in words:
            wordmap.setdefault(w, 0)
            wordmap[w] += 1

        for k, v in wordmap.items():
            yield k, v

    def reducer(self, key, values):
        yield key, sum(values)


class MRWordCount3(MRJob):

    def mapper_init(self):
        self.wordmap = {}

    def mapper(self, _, line):
        words = line.split(" ")
        for w in words:
            self.wordmap.setdefault(w, 0)
            self.wordmap[w] += 1

    def mapper_final(self):
        for k, v in self.wordmap.items():
            yield k, v

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRWordCount3.run()