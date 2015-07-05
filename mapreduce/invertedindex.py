__author__ = 'vamshi'

from mrjob.job import MRJob

class MRInvertedIndex(MRJob):
    def mapper(self, _, line):
        arr = line.split(" ")
        for w in arr[1:]:
            yield w, arr[0]

    def combiner(self, key, values):
        yield key, " ".join(set(values))

    def reducer(self, key, values):
        yield key, " ".join(set(values))

if __name__ == '__main__':
    MRInvertedIndex.run()