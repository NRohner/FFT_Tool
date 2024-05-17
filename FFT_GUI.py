import math
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk, font, END
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style
import tkinter.messagebox
import pandas as pd
import pathlib
from queue import Queue
from PIL import Image, ImageTk

# Class Definitions
class Application(tkinter.Tk):
     def __init__(self):
            super().__init__()
            self.title('FFT Tool')
            self.style = Style('litera')
            self.window = MainWindow(self, padding=10)
            self.window.pack(fill='both', expand='yes')

            # Set the window size to 600x300
            self.geometry('600x350')


class MainWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables
        self.csv_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()))

        # Boolean variables for error proofing
        self.has_analyzed = False

        self.infoText = ""
        self.acceleration = np.empty(1)
        self.time = np.empty(1)
        self.f_plot = np.empty(1)
        self.A_mag_plot = np.empty(1)

        self.sc1 = None
        self.sc2 = None

        # Frame for the logo and application title
        titleFrame = ttk.Frame(self)
        titleFrame.pack(side='top', fill='x')

        # Adding the Application title label
        titleFont = font.Font(family='ABBvoice', size=24)
        applicationTitle = ttk.Label(titleFrame, text='FFT Tool', font=titleFont)
        applicationTitle.pack(side='right')

        # container for user input
        input_labelframe = ttk.Labelframe(self, text='Select a CSV file', padding=(20, 10, 10, 5))
        input_labelframe.pack(side='top', fill='x')
        input_labelframe.columnconfigure(1, weight=1)

        # container for calculate
        calculate_labelframe = ttk.Frame(self)
        calculate_labelframe.pack(side='top', fill='x')
        calculate_labelframe.columnconfigure(1, weight=1)

        # container for info text box
        info_labelframe = ttk.Labelframe(self, text='Info', padding=(20, 10, 10, 5))
        info_labelframe.pack(side='top', fill='both')
        info_labelframe.columnconfigure(1, weight=1)

        # csv path input
        ttk.Label(input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(input_labelframe, textvariable=self.csv_path_var)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='Browse', command=self.on_in_browse, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # Calculate button
        calculate_button = ttk.Button(calculate_labelframe, text='Calculate FFT', command=self.computeFFT, style='success.Tbutton')
        calculate_button.pack(pady=20)

        # Info Text Output Box
        self.infoTextBox = ScrolledText(info_labelframe)
        self.infoTextBox.pack()


    def on_in_browse(self):
        path = askopenfilename(title="Select a CSV file", filetypes=[("CSV Files", "*.csv; *.CSV")])
        if path:
            self.csv_path_var.set(path)

        self.has_analyzed = False


    def plotFFT(self):
        fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)

        # First plotting a scatter plot so the picker works nicely
        self.sc1 = ax1.scatter(self.time, self.acceleration, picker=True, alpha=0)
        self.sc2 = ax2.scatter(self.f_plot, self.A_mag_plot, picker=True, alpha=0)

        # Now plotting the lines between the points
        ax1.plot(self.time, self.acceleration, linestyle='-', color='blue', alpha=1)
        ax2.plot(self.f_plot, self.A_mag_plot, linestyle='-', color='red', alpha=1)

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
        fig.canvas.mpl_connect('pick_event', self.on_pick)
        plt.show()

    # Plot Point Selector
    def on_pick(self, event):
        if event.artist == self.sc1:  # Check if the pick event is associated with the first scatter plot
            index = event.ind[0]
            selected_point = (round(self.time[index], 3), round(self.acceleration[index], 3))
            print(f'Selected point in Acceleration plot: {selected_point}\n')
            self.infoTextBox.insert(END, f'Selected point in Acceleration plot: {selected_point}' + "\n")


        elif event.artist == self.sc2:  # Check if the pick event is associated with the second scatter plot
            index = event.ind[0]
            selected_point = (round(self.f_plot[index], 3), round(self.A_mag_plot[index], 3))
            print(f'Selected point in Frequency plot: {selected_point}')
            self.infoTextBox.insert(END, f'Selected point in Frequency plot: {selected_point}' + "\n")


    # Load csv file and compute the FFT
    def computeFFT(self):
        # Load the CSV
        csvData = pd.read_csv(self.csv_path_var.get())

        # Save the columns to an array
        self.time = np.array(csvData.iloc[:, 0])
        self.acceleration = np.array(csvData.iloc[:, 1])

        # Calculating a few important variables (time step, sample rate, # of samples, ect.)
        timeStep = self.time[1] - self.time[0]
        sampleFrequency = 1 / timeStep
        numSamples = len(self.time)

        frequencyStep = sampleFrequency / numSamples  # Frequency steps for our frequency domain plots
        f = np.linspace(0, (numSamples - 1) * frequencyStep, numSamples)  # Establishing the frequency array (the X axis of our frequency domain plot)

        # Perform the FFT
        A = np.fft.fft(self.acceleration)  # Taking the FFT of our acceleration data. Output will be an array of complex numbers
        A_mag = np.abs(A) / numSamples  # We only care about the magnitude of this output vector. We also need to normalize it by dividing by the number of samples

        self.f_plot = f[0:int(numSamples / 2 + 1)]  # Splitting our frequency array in half to accommodate Nyquist Theorem
        self.A_mag_plot = 2 * A_mag[0:int(numSamples / 2 + 1)]  # Same thing, splitting in half
        self.A_mag_plot[0] = self.A_mag_plot[0] / 2  # Note: DC component does not need to be multiplied by 2. The DC component (or the portion with a frequency of 0 aka a constant) needs to be accounted for here

        self.plotFFT()

        self.has_analyzed = True


# Running the main application
if __name__ == '__main__':
    file_queue = Queue()
    searching = False
    Application().mainloop()