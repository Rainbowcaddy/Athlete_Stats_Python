import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
# Paths to the Excel files



# Updated paths to the new Excel files
# Updated paths to the new Excel files with improved data
excel_files = [
    'excel/nonlinear_vertical_jump.xlsx', 
    'excel/nonlinear_shot_put.xlsx', 
    'excel/nonlinear_squat.xlsx', 
    'excel/nonlinear_long_jump.xlsx', 
    'excel/nonlinear_100m_sprint.xlsx'
]

print(excel_files)
# Exercise names corresponding to each file
exercise_names = ['Vertical Jump', 'Shot Put', 'Squat', 'Long Jump', '100m Sprint']

# Read each file and add an exercise column
dataframes = []
for file, exercise in zip(excel_files, exercise_names):
    df = pd.read_excel(file)
    df['Exercise'] = exercise  # Adding exercise name as a separate column
    dataframes.append(df)

# Concatenate all DataFrames into one
master_dataframe = pd.concat(dataframes, ignore_index=True)

# Convert 'Event Date' to datetime
master_dataframe['Event Date'] = pd.to_datetime(master_dataframe['Event Date'])

print(master_dataframe[300:325])
# Analysis 1: Individual vs Everyone Else
def plot_performance_comparison(data, exercise, individual_name):
    # Filter the DataFrame for the selected exercise
    exercise_data = data[data['Exercise'] == exercise]

    # Calculate the average performance for the selected individual
    individual_avg = exercise_data[exercise_data['Name'] == individual_name][exercise].mean()

    # Calculate the average performance for others
    others_avg = exercise_data[exercise_data['Name'] != individual_name][exercise].mean()

    # Plotting
    plt.figure(figsize=(8, 6))
    bars = plt.bar([individual_name, "Others"], [individual_avg, others_avg], color=['blue', 'orange'])
    
    # Adding the text on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    plt.ylabel(exercise)
    plt.title(f'Average Performance Comparison in {exercise}')
    plt.show()



def plot_individual_performance_over_time(data, individual_name, exercise):
    individual_data = data[(data['Name'] == individual_name) & (data['Exercise'] == exercise)].sort_values('Event Date')
    plt.plot(individual_data['Event Date'], individual_data[exercise])
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

# Create the main window
root = tk.Tk()
root.title("Athlete Performance Analysis")
root.geometry("500x350")  # Adjust the size of the window

# Set a theme and configure style
style = ttk.Style(root)
style.theme_use('clam')  # Using 'clam' theme

# Configure the style for labels, buttons, and comboboxes
style.configure('TLabel', font=('Helvetica', 12), background='light gray', foreground='blue')
style.configure('TButton', font=('Helvetica', 12), background='light blue')
style.configure('TCombobox', font=('Helvetica', 12), fieldbackground='white', foreground='black')

# Set background color for the window
root.configure(bg='light gray')

# Title Label
title_label = ttk.Label(root, text="Athlete Stats", font=('Helvetica', 16, 'bold'), background='light gray', foreground='dark blue')
title_label.pack(pady=10)

# Dropdown for selecting a name
name_var = tk.StringVar()
name_label = ttk.Label(root, text="Select a Name:", background='light gray', foreground='black')
name_label.pack(pady=5)
name_dropdown = ttk.Combobox(root, textvariable=name_var, width=40, font=('Helvetica', 12))
name_dropdown['values'] = list(master_dataframe['Name'].unique())
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
exercise_dropdown['values'] = exercise_names
exercise_dropdown.pack(pady=5)

# Button to update the plot
update_button = ttk.Button(root, text="Update Plot", command=update_plot)
update_button.pack(pady=10)

# Run the application
root.mainloop()