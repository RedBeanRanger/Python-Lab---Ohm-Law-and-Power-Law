# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:10:03 2021

@author: angel
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# Read the file
v, v_err, c, c_err = np.loadtxt(r"C:\Users\angel\Desktop\Docs\PHY244\PowerLawOhmLawLab\lightbulbData1.csv", 
                                                              delimiter = ",", unpack = True)

#truncate all the points
c = c[3:]
v = v[3:]
c_err = c_err[3:]
v_err = v_err[3:]

c_amps = c/1000 # convert current into amps
c_err_amps = c_err/1000 # get current uncertainty in amps
c_log = np.log(c_amps) # take the log of current
v_log = np.log(v) # take the log of voltage

#c_err_log = (c_err_amps/(c_amps))*math.log(math.e, 10) # error propogation for log
c_err_log = (c_err_amps/(c_amps))
#v_err_log = (v_err/v)*math.log(math.e, 10)
v_err_log = (v_err/v)


plt.errorbar(v_log, c_log, yerr = c_err_log, xerr = v_err_log, marker = "o", ls = "none", label = "Data")
plt.title("Log of Current Over Log of Voltage (Linear Regression)")
plt.xlabel("Log of Voltage (log(V))")
plt.ylabel("Log of Current (log(Amps))")


# Model function
def calcCurrentLogarithmic(voltage, b, a): 
    # given a logarithmic voltage, return a logarithmic current according to power law
    return (b*voltage) + a

# Create model data using curvefit
# With sigma
popt1, pcov1 = curve_fit(calcCurrentLogarithmic, xdata = v_log, ydata = c_log,
                       sigma = c_err_log, absolute_sigma = True)
pstd1 = np.sqrt(np.diag(pcov1))
print("The paremeters of curve fit are: ", popt1)
print("The standard deviation of the model data is", pstd1, "\n")


# Without sigma
"""
popt2, pcov2 = curve_fit(calcCurrentLogarithmic, xdata = v_log, ydata = c_log,
                       bounds =[(min(v_log), min(c_log)), (max(v_log), max(c_log))])
pstd2 = np.sqrt(np.diag(pcov2))
print("The paremeters of curve fit 2 are: ", popt2)
print("The standard deviation of Curve Fit 2 is", pstd2)
"""


model_current_data1 = []
#model_current_data2 = []
for i in range(0, len(v_log)):
        model_current_data1.append(calcCurrentLogarithmic(v_log[i], popt1[0], popt1[1]))
#        model_current_data2.append(calcCurrentLogarithmic(v_log[i], popt2[0], popt2[1]))
        
# Reduced chi square calculation

def redChiSquared(measured_data, predicted_data, err):
    # returns chiSquared value
    # takes in arrays of measured_data, predicted_data, and err
    # assume the arrays have the same length
    sum = 0
    for x in range(0, len(measured_data)):
        #sum += ((10**(measured_data[x]) - 10**(predicted_data[x])) / 10**(err[x]))**2
        sum += (((measured_data[x]) - (predicted_data[x])) / (err[x]))**2
    return sum/(len(measured_data) - 2)
        

#logarithmically scaled reduced chi
print ("The reduced chi squared of Curve Fit 1 is", redChiSquared(c_log, model_current_data1, c_err_log))
#print ("The reduced chi squared of Curve Fit 2 is", redChiSquared(c_log, model_current_data2, c_err_log))
# Graph the model data

curveFitLabel = "log(current) =" + str(round(popt1[0],3)) +  "ln(voltage) + ln(" + str(round(popt1[1],3)) + ")"
plt.errorbar(v_log, model_current_data1, label = curveFitLabel)
#plt.errorbar(v_log, model_current_data2, label = "Curve Fit 2 (without sigma)")
plt.legend()