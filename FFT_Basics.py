import math

import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from ttkbootstrap import Style
import tkinter.messagebox


# Project Outline
# 1. Get the fundamental math and plotting portions squared away
# 2. Get csv importing handled
# 3. Create a GUI
# 4. Create .exe





# Math Testing

# Input signal - time based
Fs = 2000   # Sampling Frequency
tStep = 1 / Fs      # Sample time interval
f0 = 100            # Signal frequency

N = int(10 * Fs / f0)         # Number of samples

t = np.linspace(0, (N-1) * tStep, N)        # These are the time steps of the time domain
fstep = Fs / N                              # Frequency Interval
f = np.linspace(0, (N-1) * fstep, N)        # Frequency Steps

y = 1 * np.sin(2 * np.pi * f0 * t) + np.cos(2 * np.pi * 500 * t)          # This is our input signal. Sin wave with an amplitude of 1 and a frequency of f0


# Perform FFT

X = np.fft.fft(y)       # Pretty simple, to get the FFT you just pass it the values of the time domain signal. X will be a series of complex numbers
X_mag = np.abs(X) / N   # We only care about the magnitude of X. We also need to normalize it by dividing by the total number of samples

# IMPORTANT - You can only accurately reconstruct the frequency domain up to HALF the frequency of the sampling frequency. Look into Nyquist Theorem

f_plot = f[0:int(N/2+1)]
X_mag_plot = 2 * X_mag[0:int(N/2+1)]
X_mag_plot[0] = X_mag_plot[0] / 2       # Note: DC component does not need to be multiplied by 2. The DC component (or the portion with a frequency of 0 aka a constant) needs to be accounted for here



# Plot both signals

fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
ax1.plot(t, y, '.-')
ax2.plot(f_plot, X_mag_plot, '.-')
plt.show()
