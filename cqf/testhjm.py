import yaml
with open('testhjm.yaml', 'r') as f:
    doc = yaml.load(f)

freq_map = {"Monthly": 0.0833333, "Quarterly": 0.25, "SemiAnnually": 0.5, "Yearly": 1.0}

principal = doc["hjm_testcase"]["Principal"]
product = doc["hjm_testcase"]["Product"]
maturity = doc["hjm_testcase"]["Maturity"]
int_rate = doc["hjm_testcase"]["InterestRate"]
freq = freq_map[doc["hjm_testcase"]["Frequency"]]
factors = doc["hjm_testcase"]["Factors"]
nsims = doc["hjm_testcase"]["NoOfSimulations"]

from hjm.hjmpricer import *
hjmp = HJMPricer(principal, product, maturity, int_rate, freq, factors, nsims)
(price, sims), pca = hjmp.getHjmPrice()
print "The parameters for HJM test case are:"
print "Principal:", principal
print "Product:", product
print "Maturity:", maturity
print "Interest rate:", int_rate
print "Frequency:", freq
print "No of simulations:", nsims
print "The price of the instrument is:", price

