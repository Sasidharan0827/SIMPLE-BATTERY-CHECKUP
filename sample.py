import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import uuid
import barcode
from barcode.writer import ImageWriter
from impedance import preprocessing
from impedance.models.circuits import CustomCircuit
from impedance.visualization import plot_nyquist
import matplotlib.pyplot as plt

def generate_barcode(cell_id):
    # Generate barcode using Code128 format
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(cell_id, writer=ImageWriter())
    barcode_path = f"{cell_id}.png"  # Save barcode with Cell_ID as filename
    barcode_instance.save(barcode_path)

    return barcode_path

def upload_image_and_display():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # Display the selected image in the graph window
            image = Image.open(file_path)
            image = image.resize((200, 200))  # Resize the image if needed
            photo = ImageTk.PhotoImage(image)

            # Update the image in the label
            label_image.config(image=photo)
            label_image.image = photo

            # Generate unique Cell_ID
            cell_id = str(uuid.uuid4().int)[:10]
            cell_id_label.config(text=f"Cell ID: {cell_id}")
            cell_id_label.pack()

            # Generate barcode
            barcode_path = generate_barcode(cell_id)
            barcode_label.config(text=f"Barcode saved as: {barcode_path}")
            barcode_label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the image: {str(e)}")

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

def upload_csv_and_process():
    file_path = filedialog.askopenfilename()
    if file_path:
        frequencies, Z = process_csv(file_path)
        if frequencies is not None and Z is not None:
            fit_and_plot(frequencies, Z)


root = tk.Tk()
root.title("Nyquist Plot")
root.configure(bg="black")



heading_label = tk.Label(root, text="Simple Battery Checkup", font = ("Times New Roman", 80), fg="white",bg="black")
heading_label.pack(pady=10)  # Add some padding to the top
paragraph_text = "A web interface for displaying battery cell information. Users can upload a representative image of the cell and automatically generate a unique 10-digit Cell_ID and Bar Code for identification. Meta information such as cell condition, electrical parameters, and data upload options are provided. The webpage utilizes a Python library to transform the data and generate Bode plots, an Equivalent Circuit Model, and State-of-the-Health (SoH) indicators, enhancing data visualization and analysis for users."
paragraph_label = tk.Label(root, text=paragraph_text, font=("Times New Roman", 20), fg="white", bg="black", padx=40, pady=50, wraplength=1500, justify="left")
paragraph_label.pack()
label_image = tk.Label(root, bg="black")
label_image.pack(side="left", padx=20, pady=(50, 10))

cell_id_label = tk.Label(root, bg="black", fg="white")
cell_id_label.pack(side="left", padx=(10, 10), pady=(0, 10), anchor="nw")


barcode_label = tk.Label(root, bg="black", fg="white")
barcode_label.pack(side="left", padx=(10, 10), pady=(0,10), anchor="nw")
your_text_label = tk.Label(root, text=" upload your battery image", font=("Times New Roman", 16), fg="white", bg="black", pady=10)
your_text_label.pack()


upload_image_button = tk.Button(root, text="Upload Image", command=upload_image_and_display, bg="blue", fg="white", padx=10, pady=5, font=("Times New Roman", 12, "bold"), width=20, height=2)
upload_image_button.pack()

def open_form_window():

    form_window = tk.Toplevel(root)
    form_window.title("Battery Information Form")
    form_window.configure(bg="black")

    
    form_entries = [
        ("Cell Condition (New or Recycled):", ""),
        ("Manufacturer:", ""),
        ("Model:", ""),
        ("Type:", ""),
        ("Chemistry:", ""),
        ("Shape:", ""),
        ("Weight (g):", ""),
        ("Height (mm):", ""),
        ("Diameter (mm):", ""),
        ("Volume (cm³):", "")
    ]

    entries = []  # List to store entry widgets for future use

    for row, (label_text, default_value) in enumerate(form_entries):
        label = tk.Label(form_window, text=label_text, font=("Times New Roman", 14), fg="white", bg="black")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(form_window)
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, padx=10, pady=5)

        
        entries.append(entry)

 
    def get_form_data():
        form_data = {}
        for entry, (label_text, _) in zip(entries, form_entries):
            form_data[label_text] = entry.get()
        print(form_data)  # Just for testing, you can replace this with your desired action
        form_window.destroy()  # Close the form window

   
    submit_button = tk.Button(form_window, text="Submit", command=get_form_data)
    submit_button.grid(row=len(form_entries), columnspan=2, pady=(10, 20))

def open_battery_info_form():
   
    your_text_label = tk.Label(root, text=" fill your battery details", font=("Times New Roman", 16), fg="white", bg="black", pady=10)
    your_text_label.pack()
    open_form_button = tk.Button(root, text="Open Battery Information Form", command=open_form_window, bg="blue", fg="white", padx=10, pady=5, font=("Times New Roman", 12, "bold"), width=20, height=2)
    open_form_button.pack(pady=10)
    

open_battery_info_form()
your_text_label = tk.Label(root, text=" upload your battery frequency and impedance in csv file format", font=("Times New Roman", 16), fg="white", bg="black", pady=10)
your_text_label.pack()

upload_csv_button = tk.Button(root, text="Upload CSV and Process", command=upload_csv_and_process, bg="blue", fg="white", padx=10, pady=5, font=("Times New Roman", 12, "bold"), width=20, height=2)
upload_csv_button.pack()

root.mainloop()
