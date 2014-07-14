#__author__ = 'vamshi'
from scipy.stats import norm, chi2, t
import numpy
cimport numpy
from libc.math cimport sqrt

DTYPE = numpy.double
ctypedef numpy.double_t DTYPE_t


cdef class GaussianCopula:
    cdef object random_state
    cdef int dimension
    cdef numpy.ndarray covariance, cholesky_factor

    def __init__(self, numpy.ndarray[double,ndim=2] covariance):
        self.covariance = covariance
        self.random_state = numpy.random.RandomState()
        self.dimension = len(self.covariance[0])
        self.cholesky_factor = numpy.linalg.cholesky(self.covariance)

    def simulate(self):
        cdef numpy.ndarray[double, ndim=1] z = self.random_state.normal(loc=0.0, scale=1.0, size=(self.dimension, ))
        cdef numpy.ndarray[double, ndim=1] x = numpy.dot(self.cholesky_factor, z)
        for i in range(self.dimension):
            x[i] = norm.cdf(x[i], loc=0.0, scale=1.0)
        return x


cdef class StudentTCopula:
    cdef int dimension
    cdef numpy.ndarray covariance, cholesky_factor, sigma, sigmaInverse
    cdef double determinant, nu

    def __init__(self, numpy.ndarray[double, ndim=2] covariance,double nu):
        self.covariance = covariance
        self.dimension = self.covariance[0].size
        self.cholesky_factor = numpy.linalg.cholesky(self.covariance)
        self.sigma = numpy.array(covariance)
        self.sigmaInverse = numpy.linalg.inv(self.sigma)
        self.determinant = numpy.linalg.det(self.sigma)
        self.nu = nu

    def simulate(self):
        cdef numpy.ndarray[double, ndim=1] z = norm.rvs(loc=0.0, scale=1.0, size=self.dimension)
        cdef numpy.ndarray[double, ndim=1] x = numpy.dot(self.cholesky_factor, z)
        cdef double s = chi2.rvs(self.nu, size=1)[0]
        for i in range(self.dimension):
            x[i] = t(self.nu).cdf(x[i] * sqrt(self.nu / s))
        return x


