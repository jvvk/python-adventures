__author__ = 'vamshi'
from mrjob.job import MRJob
from math import sqrt

class MRMinMaxCount(MRJob):
    def mapper(self, _, line):
        yield "Num", line

    def reducer(self, key, values):
        count, minv, maxv = 0, float("inf"), float("-inf")
        for v in values:
            fv = float(v)
            count += 1
            minv = fv if (fv < minv) else minv
            maxv = fv if (fv > maxv) else maxv
        yield "Min-Max-Count", (minv, maxv, count)

class MRMedianStdDev(MRJob):
    def mapper(self, _, line):
        yield "Num", line

    def reducer(self, key, values):
        count, s = 0, 0
        lv = []
        for v in values:
            fv = float(v)
            s += fv
            lv.append(fv)
            count += 1
        lv.sort()
        median =  lv[int(count/2)] if (count % 2 != 0) else (lv[count/2] + lv[int(count/2) -1])/2.0
        avg = s / count
        sumOfSquares = 0.0
        for f in  lv:
            sumOfSquares += (f - avg) * (f - avg)
        stddev = sqrt(sumOfSquares/(count-1))
        yield "median-stddev", (median, stddev)


if __name__ == '__main__':
    MRMinMaxCount.run()
    MRMedianStdDev.run()