# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 01:58:19 2021

@author: angel
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read the file
v, v_err, c, c_err = np.loadtxt(r"C:\Users\angel\Desktop\Docs\PHY244\PowerLawOhmLawLab\PotentiometerData.csv", 
                                                              delimiter = ",", unpack = True)

# convert current to amps
c_amps = c/1000
c_err_amps = c_err/1000

# Make the errorbar plot for data points
plt.errorbar(v, c_amps, yerr = c_err_amps, xerr = v_err, marker = "o", ls = "none", label = "Data")
plt.title("Curent Over Voltage for Unknown Potentiometer")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (Amps)")

# Model function

def ohmsLaw(voltage, r):
    # Given voltage (V) and resistance (Ohms), returns current (Amps)
    # I = V/R
    return voltage/r

popt, pcov = curve_fit(ohmsLaw, xdata = v, ydata = c_amps)

model_data = []

for x in range(0, len(v)):
    model_data.append(ohmsLaw(v[x], popt[0]))

model_data = np.array(model_data)

def redChiSquared(measured_data, predicted_data, err):
    # returns chiSquared value
    # takes in arrays of measured_data, predicted_data, and err
    # assume the arrays have the same length
    sum = 0
    for x in range(0, len(measured_data)):
        sum += ((measured_data[x]) - (predicted_data[x]))**2 / (err[x])**2
    return sum/len(measured_data)

print("The reduced chi squared value of this fitted curve is ", redChiSquared(c_amps, model_data, c_err_amps))

plt.plot(v, model_data, label = "Curve fit, Resistance = 4809.582 Ohms")
print("Resistance = " + str(round(popt[0],3)) + " Ohms")

plt.legend()