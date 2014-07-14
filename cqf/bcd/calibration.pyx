__author__ = 'vamshi'
from scipy.stats import norm, kendalltau, t
from scipy.special import gammaln
from distribution import EmpiricalDistribution
from bcd.copula import GaussianCopula, StudentTCopula
import numpy
from math import pi

cimport numpy
from libc.math cimport sqrt, sin, log


DTYPE = numpy.double
ctypedef numpy.double_t DTYPE_t


def returns(numpy.ndarray[double, ndim=2] adjusted_prices):
    cdef int dimension, no_of_observations,i, j
    cdef numpy.ndarray[double, ndim=2] returns
    dimension, no_of_observations = len(adjusted_prices), len(adjusted_prices[0])
    returns = numpy.zeros((dimension, no_of_observations - 1))
    for i in range(dimension):
        for j in range(1, no_of_observations):
            returns[i, j-1] = log(adjusted_prices[i, j]/adjusted_prices[i, j-1])
    return returns


def transformed_variates(numpy.ndarray[double, ndim=2] observations):
    cdef int dimenstion, no_of_observations, i, j
    cdef numpy.ndarray[double,ndim=2] variates
    cdef object marginal
    dimension, no_of_observations = len(observations), len(observations[0])
    variates = numpy.zeros((dimension, no_of_observations))
    for i in range(dimension):
        marginal = EmpiricalDistribution(observations[i])
        for j in range(no_of_observations):
            variates[i, j] = norm.ppf(marginal.cdf(observations[i, j]))
    return variates


def uniform_variates(numpy.ndarray[double, ndim=2] observations):
    cdef int dimension, no_of_observations,i,j
    cdef numpy.ndarray[double, ndim=2] variates
    cdef object marginal
    dimension,  no_of_observations = len(observations), len(observations[0])
    variates = numpy.zeros((dimension, no_of_observations))
    for i in range(dimension):
        marginal = EmpiricalDistribution(observations[i])
        for j in range(no_of_observations):
            variates[i, j] = marginal.cdf(observations[i, j])
    return variates

def transformedTVariates(numpy.ndarray[double, ndim=2] observations):
    cdef int dimension, no_of_observations,i,j
    cdef numpy.ndarray[double, ndim=2] variates
    cdef object marginal
    dimension, noOfObservations = len(observations), len(observations[0])
    variates = numpy.zeros((dimension, noOfObservations))
    for i in range(dimension):
        marginal = EmpiricalDistribution(observations[i])
        for j in range(noOfObservations):
            variates[i, j] = marginal.cdf(observations[i, j])
    return variates


cdef class GaussianCalibrator:
    def calibrate(self, numpy.ndarray[double, ndim=2] adjustedPrices):
        return self.calibrate_from_returns(returns(adjustedPrices))

    def calibrate_from_returns(self, numpy.ndarray[double, ndim=2] returns):
        return self.calibrate_from_variates(transformed_variates(returns))

    def calibrate_from_variates(self, numpy.ndarray[double, ndim=2] variates):
        cdef int dimension, no_of_observations,i,j,k
        cdef numpy.ndarray[double, ndim=2] covariance
        cdef double tot
        dimension, no_of_observations = len(variates), len(variates[0])
        covariance = numpy.zeros((dimension, dimension))
        for i in range(dimension):
            for j in range(i+1):
                tot = 0.0
                for k in range(no_of_observations):
                    tot += variates[i, k]*variates[j, k]
                covariance[i, j] = tot/no_of_observations
                covariance[j, i] = covariance[i, j]
        return GaussianCopula(covariance)


cdef class StudentTCalibrator:
    MAXIMUM_NU_VALUE = 10.0
    DELTA = 0.2
    cdef double maximumNuValue, delta

    def __init__(self, double maximumNuValue,double delta):
        self.maximumNuValue = maximumNuValue
        self.delta = delta

    def calibrate(self, numpy.ndarray[double, ndim=2] adjustedPrices):
        return self.calibrateFromReturns(returns(adjustedPrices))

    def calibrateFromReturns(self, numpy.ndarray[double, ndim=2] returns):
        return self.calibrateFromVariates(transformedTVariates(returns))

    def calibrateFromVariates(self, numpy.ndarray[double, ndim=2] variates):
        cdef int dimension, no_of_observations
        cdef numpy.ndarray[double, ndim=2] covarianceData, sigma
        cdef double nu
        dimension, noOfObservations = len(variates), len(variates[0])
        covarianceData = self.covariance(variates)
        sigma = numpy.array(covarianceData)
        nu = self.optimalNu(variates, sigma, covarianceData)
        return StudentTCopula(covarianceData, nu)

    def covariance(self,numpy.ndarray[double, ndim=2] variates):
        cdef int dimension, no_of_observations,i,j
        cdef numpy.ndarray[double, ndim=2] covarianceData
        cdef double nu, tau, pv
        dimension, noOfObservations = len(variates), len(variates[0])
        covarianceData = numpy.zeros([dimension, dimension])
        for i in range(dimension):
            for j in range(i + 1):
                tau, pv = kendalltau(variates[i], variates[j])
                covarianceData[i, j] = sin(pi/2.0 * tau)
                covarianceData[j, i] = covarianceData[i, j]
        return covarianceData

    def optimalNu(self,numpy.ndarray[double, ndim=2] variates,numpy.ndarray[double, ndim=2] sigma,numpy.ndarray[double, ndim=2] covariance):
        cdef int dimension, no_of_observations,i,j
        cdef numpy.ndarray[double, ndim=2] sigmaInverse
        cdef double nu,argMax, maxValue, a,b, value,ld, determinant
        dimension, noOfObservations = len(variates), len(variates[0])
        sigmaInverse = numpy.linalg.inv(sigma)
        determinant = numpy.linalg.det(sigma)
        nu = 2.0
        argMax = 0.0
        maxValue = float("-inf")
        while nu <= self.maximumNuValue:
            a = gammaln(0.5 * (nu + dimension)) - gammaln(0.5 * nu) - 0.5 * dimension * log(nu)
            b = 0.5 * (dimension * log(pi) + log(determinant))
            tCopula = StudentTCopula(covariance, nu)
            value = 0.0
            ld = 0.0
            for j in range(noOfObservations):
                variate = numpy.zeros(dimension)
                for i in range(dimension):
                    variate[i] = t.ppf(variates[i, j], nu)
                    ld += log(t.pdf(variate[i], nu))
                variateVector = numpy.array(variate)
                value += log(1.0 + numpy.dot(variateVector, numpy.dot(sigmaInverse, variateVector)) / nu)
            value = noOfObservations * (a - b) - 0.5 * (nu + dimension) * value - ld
            if value > maxValue:
                maxValue = value
                argMax = nu
            nu += self.delta
        return argMax

