__author__ = 'twisa'

from mrjob.job import MRJob


def sum_pairs(x, y):
    return (x[0] + y[0], x[1] + y[1])


class MRAvg1(MRJob):
    def mapper(self, _, line):
        k = line[15:21]
        v = line[87:92]
        yield (k, (int(v), 1))

    def reducer(self, key, values):
       s, n = reduce(sum_pairs, values)
       yield key, (s/n)

class MRAvg2(MRJob):
    def mapper(self, _, line):
        k = line[15:21]
        v = line[87:92]
        yield (k, (int(v), 1))

    def combiner(self, key, values):
        s, n = reduce(sum_pairs, values)
        yield key, (s, n)

    def reducer(self, key, values):
       s,n = reduce(sum_pairs, values)
       yield key, (s/n)


class MRAvg3(MRJob):
    def mapper_init(self):
        self.s = {}
        self.c = {}

    def mapper(self, _, line):
        k = line[15:21]
        v = line[87:92]
        self.s.setdefault(k, 0)
        self.c.setdefault(k, 0)
        self.s[k] += int(v)
        self.c[k] += 1

    def mapper_final(self):
        for k in self.s.keys():
            yield (k, (self.s[k], self.c[k]))

    def combiner(self, key, values):
        s, n = reduce(sum_pairs, values)
        yield key, (s, n)

    def reducer(self, key, values):
       s,n = reduce(sum_pairs, values)
       yield key, (s/n)


if __name__ == '__main__':
    MRAvg3.run()