import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
from impedance import preprocessing
from impedance.models.circuits import CustomCircuit
from impedance.visualization import plot_nyquist

def process_csv(file_path):
    try:
        frequencies, Z = preprocessing.readCSV(file_path)
        frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)
        return frequencies, Z
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the CSV file: {str(e)}")

def fit_and_plot(frequencies, Z):
    try:
        circuit = 'R0-p(R1,C1)-p(R2-Wo1,C2)'
        initial_guess = [.01, .01, 100, .01, .05, 100, 1]

        circuit = CustomCircuit(circuit, initial_guess=initial_guess)
        circuit.fit(frequencies, Z)
        Z_fit = circuit.predict(frequencies)

        fig, ax = plt.subplots(figsize=(12, 8))
        plot_nyquist(Z, fmt='o', scale=10, ax=ax)
        plot_nyquist(Z_fit, fmt='-', scale=10, ax=ax)

        plt.legend(['Data', 'Fit'])
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fitting and plotting: {str(e)}")

def upload_and_process():
    file_path = filedialog.askopenfilename()
    if file_path:
        frequencies, Z = process_csv(file_path)
        if frequencies is not None and Z is not None:
            fit_and_plot(frequencies, Z)

# Create a tkinter window
root = tk.Tk()
root.title("Nyquist Plot")

# Create a button to upload CSV file and process data
upload_button = tk.Button(root, text="Upload CSV and Process", command=upload_and_process)
upload_button.pack()

# Start the tkinter event loop
root.mainloop()
