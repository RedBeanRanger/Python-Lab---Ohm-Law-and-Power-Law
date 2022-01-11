# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 12:38:16 2021

@author: angel
"""

import numpy as np
from math import log
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read the file
v, v_err, c, c_err = np.loadtxt(r"C:\Users\angel\Desktop\Docs\PHY244\PowerLawOhmLawLab\lightbulbData1.csv", 
                                                              delimiter = ",", unpack = True)

# take the log of current and voltage
c_log = np.log(c/1000)
v_log = np.log(v)

### calculate uncertainty to log scale
c_err_scaled = (c_err/1000/c)
#c_err_scaled = (np.log(c + c_err) - np.log(c - c_err))/2
v_err_scaled = v_err/(v)
#v_err_scaled = (np.log(v + v_err) - np.log(v - v_err))/2


# Make the errorbar plot for data points
plt.errorbar(v_log, c_log, yerr = c_err_scaled, xerr = v_err_scaled, marker = "o", ls = "none", label = "Data")
plt.title("Log of Current Over Log of Voltage (Linearized Power Law Relationship)")
plt.xlabel("Log of Voltage (log(V))")
plt.ylabel("Log of Current (log(Amps))")


# Model function
def calcCurrentLogarithmic(voltage, a, b): 
    # given a logarithmic voltage, return a logarithmic current according to power law
    return (a*voltage) + b


# Fit the data with a best-fit curve 
# I made two curves, the first curve does not take sigma values into account
# the second curve takes the sigma values into account
popt1, pcov1 = curve_fit(calcCurrentLogarithmic, xdata = v_log, ydata = c_log)
pstd1 = np.sqrt(np.diag(pcov1))

print("The standard deviations of curvefit 1 is", pstd1)
"""
popt2, pcov2 = curve_fit(calcCurrentLogarithmic, xdata = v_log, ydata = c_log,
                         absolute_sigma = True, sigma= c_err_scaled, 
                         bounds=[(min(v_log), min(c_log)),(max(v_log), max(c_log))])
pstd2 = np.sqrt(np.diag(pcov2))
print("The standard deviations of curvefit 2 is", pstd2)
"""
model_current_data1 = []
#model_current_data2 = []
print(popt1)
for i in range(0, len(v_log)):
        model_current_data1.append(calcCurrentLogarithmic(log(v[i]), popt1[0], popt1[1]))

#for i in range(0, len(v)):
#        model_current_data2.append(calcCurrentLogarithmic(v_log[i], popt2[0], popt2[1]))
        
def redChiSquared(measured_data, predicted_data, err):
    # returns chiSquared value
    # takes in arrays of measured_data, predicted_data, and err
    # assume the arrays have the same length
    sum = 0
    for x in range(0, len(measured_data)):
        sum += ((10**(measured_data[x]) - 10**(predicted_data[x])) / 10**(err[x]))**2
        #sum += (((measured_data[x]) - (predicted_data[x])) / (err[x]))**2
    return sum/(len(measured_data) - 2)

#not logarithmically scaled reduced chi

print ("The reduced chi squared of Curve Fit 1 is", redChiSquared(c, model_current_data1, c_err))
#print ("The reduced chi squared of Curve Fit 2 is", redChiSquared(c, model_current_data2, c_err))

#logarithmically scaled reduced chi
print ("The reduced chi squared of Curve Fit 1 is", redChiSquared(c_log, model_current_data1, c_err_scaled))
#print ("The reduced chi squared of Curve Fit 2 is", redChiSquared(c_log, model_current_data2, c_err_scaled))

# TODO: Theoretical Curve

plt.errorbar(v, model_current_data1, label = "Curve Fit 1 (without sigma)")
#plt.errorbar(v, model_current_data2, label = "Curve Fit 2 (with sigma)")
plt.legend()

