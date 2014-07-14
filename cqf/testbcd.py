import yaml
from bcd.entity import ENTITIES, Entity
from bcd.calibration import GaussianCalibrator, StudentTCalibrator
from bcd.discounter import SimpleDiscounter
from bcd.bcdpricer import BCDPricer
from numpy import array
from math import ceil
from datetime import datetime


with open('testbcd.yaml', 'r') as f:
    doc = yaml.load(f)

freq_map = {"Monthly": 0.0833333, "Quarterly": 0.25, "SemiAnnually": 0.5, "Yearly": 1.0}

entities = doc["bcd_testcase"]["Entities"]
matdate = doc["bcd_testcase"]["MaturityDate"]
effdate = doc["bcd_testcase"]["EffectiveDate"]
freq = doc["bcd_testcase"]["Frequency"]
nsims = doc["bcd_testcase"]["NoOfSimulations"]
incAccPrem = doc["bcd_testcase"]["IncludeAccruedPremium"]
copType = doc["bcd_testcase"]["CopulaType"]
recRate = doc["bcd_testcase"]["RecoveryRate"]
k = doc["bcd_testcase"]["Seniority"]

print "The parameters for BCD test case are:"
print "Entities:", entities
print "Copula Type:", copType
print "Seniority:", k
print "Maturity Date:", matdate
print "Effective Date:", effdate
print "Frequency:", freq
print "IncludeAccruedPremium:", incAccPrem
print "Recovery Rate", recRate
print "No of simulations:", nsims


mdate = datetime.strptime(matdate, "%d/%m/%Y")
edate = datetime.strptime(effdate, "%d/%m/%Y")

def getNoOfPeriods(delta, maturityDate, effectiveDate):
     return int(ceil((maturityDate - effectiveDate).days / (365 * delta)))

marginals = []
ent_objs = []
for t in entities:
    e = Entity(ENTITIES[t],t)
    e.calibrate()
    ent_objs.append(e)
    marginals.append(e.survivalDistribution)

calib = None
if copType == "Gaussian":
    calib = GaussianCalibrator()
else:
    calib = StudentTCalibrator(10, 0.2)

pd = array([e.priceData() for e in ent_objs])
cop = calib.calibrate(pd)
noOfNames = len(entities)

delta = freq_map[freq]
noOfPeriods = getNoOfPeriods(delta, mdate, edate)
discounter = SimpleDiscounter([0.5, 1.0, 2.0, 3.0, 4.0, 5.0], [0.9932727, 0.9858018, 0.9627129, 0.9285788, 0.8891939, 0.8474275])
pricer = BCDPricer(noOfNames, k, delta, noOfPeriods, recRate, discounter, cop, marginals)
price, sims = pricer.price(nsims, incAccPrem)
print "The price of the Basket Default Swap is", price * 100.0 * 100.0