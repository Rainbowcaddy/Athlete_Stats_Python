import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, filedialog

# Function to load files and update the DataFrame
def load_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_paths:
        load_and_concatenate_files(file_paths)

def load_and_concatenate_files(file_paths):
    global master_dataframe
    dataframes = []
    for file in file_paths:
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith('.xlsx'):
            df = pd.read_excel(file)
        dataframes.append(df)

    master_dataframe = pd.concat(dataframes, ignore_index=True)
    master_dataframe['Event Date'] = pd.to_datetime(master_dataframe['Event Date'])
    update_loaded_files_label(file_paths)
    update_dropdowns()

def update_loaded_files_label(file_paths):
    loaded_files_label['text'] = "Loaded Files:\n" + "\n".join(file_paths)

def update_dropdowns():
    if 'Name' in master_dataframe:
        unique_names = master_dataframe['Name'].dropna().unique()
        name_dropdown['values'] = list(unique_names)
    # Extract all exercise columns except 'Name', 'Birth Date', and 'Event Date'
    exercise_columns = [col for col in master_dataframe.columns if col not in ['Name', 'Birth Date', 'Event Date']]
    exercise_dropdown['values'] = exercise_columns


def plot_performance_comparison(data, exercise, individual_name):
    exercise_data = data.dropna(subset=[exercise])  # Drop rows where exercise data is NaN
    individual_data = exercise_data[exercise_data['Name'] == individual_name]
    others_data = exercise_data[exercise_data['Name'] != individual_name]

    individual_avg = individual_data[exercise].mean()
    others_avg = others_data[exercise].mean()

    plt.figure(figsize=(8, 6))
    bars = plt.bar([individual_name, "Others"], [individual_avg, others_avg], color=['blue', 'orange'])
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')
    plt.ylabel(exercise)
    plt.title(f'Average Performance Comparison in {exercise}')
    plt.show()

def plot_individual_performance_over_time(data, individual_name, exercise):
    individual_data = data[data['Name'] == individual_name].sort_values('Event Date')
    plt.scatter(individual_data['Event Date'], individual_data[exercise])
    plt.title(f'Performance Over Time for {individual_name} in {exercise}')
    plt.xlabel('Event Date')
    plt.ylabel(exercise)
    plt.show()


def update_plot():
    selected_name = name_var.get()
    selected_exercise = exercise_var.get()
    analysis_type = analysis_var.get()
    if analysis_type == 'Performance Over Time':
        plot_individual_performance_over_time(master_dataframe, selected_name, selected_exercise)
    elif analysis_type == 'Performance Comparison':
        plot_performance_comparison(master_dataframe, selected_exercise, selected_name)

# ... [rest of your Tkinter UI code] ...

# ... [rest of your Tkinter UI code] ...

# Create the main window
root = tk.Tk()
root.title("Athlete Performance Analysis")
root.geometry("600x600") 

# Set a theme and configure style
style = ttk.Style(root)
style.theme_use('clam') 
style.configure('TLabel', font=('Helvetica', 12), background='light gray', foreground='blue')
style.configure('TButton', font=('Helvetica', 12), background='light blue')
style.configure('TCombobox', font=('Helvetica', 12), fieldbackground='white', foreground='black')
root.configure(bg='light gray')

# Title Label
title_label = ttk.Label(root, text="Athlete Stats", font=('Helvetica', 16, 'bold'), background='light gray', foreground='dark blue')
title_label.pack(pady=10)

# Button to load files
load_button = ttk.Button(root, text="Load CSV/Excel Files", command=load_files)
load_button.pack(pady=10)

# Label to display loaded files
loaded_files_label = ttk.Label(root, text="No files loaded", background='light gray', foreground='black')
loaded_files_label.pack(pady=10)

# Dropdown for selecting a name
name_var = tk.StringVar()
name_label = ttk.Label(root, text="Select a Name:", background='light gray', foreground='black')
name_label.pack(pady=5)
name_dropdown = ttk.Combobox(root, textvariable=name_var, width=40, font=('Helvetica', 12))
name_dropdown.pack(pady=5)

# Dropdown for selecting an analysis type
analysis_var = tk.StringVar()
analysis_label = ttk.Label(root, text="Select Analysis Type:", background='light gray', foreground='black')
analysis_label.pack(pady=5)
analysis_dropdown = ttk.Combobox(root, textvariable=analysis_var, width=40, font=('Helvetica', 12))
analysis_dropdown['values'] = ['Performance Over Time', 'Performance Comparison']
analysis_dropdown.pack(pady=5)

# Dropdown for selecting an exercise
exercise_var = tk.StringVar()
exercise_label = ttk.Label(root, text="Select an Exercise:", background='light gray', foreground='black')
exercise_label.pack(pady=5)
exercise_dropdown = ttk.Combobox(root, textvariable=exercise_var, width=40, font=('Helvetica', 12))
exercise_dropdown.pack(pady=5)

# Button to update the plot
update_button = ttk.Button(root, text="Update Plot", command=update_plot)
update_button.pack(pady=10)

# Run the application
root.mainloop()
