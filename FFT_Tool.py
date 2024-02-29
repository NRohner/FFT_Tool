import math
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from ttkbootstrap import Style
import tkinter.messagebox
import pandas as pd


# Project Outline
# 1. Get the fundamental math and plotting portions squared away
# 2. Get csv importing handled
# 3. Create a GUI
# 4. Create .exe


# Function to handle pick event in the plot

def on_pick(event):

    if event.artist == sc1:     # Check if the pick event is associated with the first scatter plot
        index = event.ind[0]
        selected_point = (t[index], accel[index])
        print(f'Selected point in Acceleration plot: {selected_point}')


    elif event.artist == sc2:   # Check if the pick event is associated with the second scatter plot
        index = event.ind[0]
        selected_point = (f_plot[index], A_mag_plot[index])
        print(f'Selected point in Frequency plot: {selected_point}')
        


# 1. Reading in CSV
csvPath = './Sample_Data/VibrData.csv'
csvData = pd.read_csv(csvPath)

# Save columns to arrays
t = np.array(csvData[csvData.columns[0]])     # Setting t = to the data stored in the first column in df
accel = np.array(csvData[csvData.columns[1]])     # Setting accel = to the data stored in the second column in df

# Calculating a few important variables (time step, sample rate, # of samples ect.)
timeStep = t[1]-t[0]
sampleFrequency = 1 / timeStep
numSamples = len(t)

frequencyStep = sampleFrequency / numSamples        # Frequency steps for our frequency domain plots
f = np.linspace(0, (numSamples - 1) * frequencyStep, numSamples)    # Establishing the frequency array (the X axis of our frequency domain plot)


# Perform the FFT
A = np.fft.fft(accel)               # Taking the FFT of our acceleration data. Output will be an array of complex numbers
A_mag = np.abs(A) / numSamples      # We only care about the magnitude of this output vector. We also need to normalize it by dividing by the number of samples


# IMPORTANT - You can only accurately reconstruct the frequency domain up to HALF the frequency of the sampling frequency. Look into Nyquist Theorem

f_plot = f[0:int(numSamples / 2 + 1)]           # Splitting our frequency array in half to accommodate Nyquist Theorem
A_mag_plot = 2 * A_mag[0:int(numSamples / 2 + 1)]  # Same thing, splitting in half
A_mag_plot[0] = A_mag_plot[0] / 2               # Note: DC component does not need to be multiplied by 2. The DC component (or the portion with a frequency of 0 aka a constant) needs to be accounted for here

print("FFT Number of Samples: ", len(A_mag_plot))
print("Raw Data Number of Samples: ", len(accel))

# Plotting

fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)

# First plotting a scatter plot so the picker works nicely
sc1 = ax1.scatter(t, accel, picker=True, alpha=0)
sc2 = ax2.scatter(f_plot, A_mag_plot, picker=True, alpha=0)

# Now plotting the lines between the points
ax1.plot(t, accel, linestyle='-', color='blue', alpha=0.75)
ax2.plot(f_plot, A_mag_plot, linestyle='-', color='red', alpha=0.75)

# Plot formatting
fig.suptitle('Data vs FFT Plot')

ax1.set_title('Acceleration')
ax1.set_xlabel('time [s]')
ax1.set_ylabel('Acceleration [mg]')
ax1.grid(True)


ax2.set_title('Frequency')
ax2.set_xlabel('Frequency [hz]')
ax2.set_ylabel('Magnitude')
ax2.grid(True)

# Connect the pick event handler to the figure
fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()