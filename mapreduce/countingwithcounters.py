__author__ = 'vamshi'

from mrjob.job import MRJob

class MRCountingWithCounters(MRJob):
    def mapper(self, _, line):
        _, group = line.split(" ")
        self.increment_counter(group, group, 1)
        yield _, _

if __name__ == '__main__':
    MRCountingWithCounters.run()