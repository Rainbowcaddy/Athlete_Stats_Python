import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import os
from tkinter.colorchooser import askcolor

def choose_color():
    global highlight_color
    color_code = askcolor(title="Choose color")[1]
    if color_code:
        highlight_color = color_code

def load_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_paths:
        load_and_concatenate_files(file_paths)

def load_and_concatenate_files(file_paths):
    global master_dataframe
    dataframes = []
    for file in file_paths:
        try:
            # Specify usecols parameter to load only the first 5 columns
            if file.endswith('.csv'):
                df = pd.read_csv(file, usecols=range(5))
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file, usecols=range(5))
            
            # After loading you might need to check if the columns are correctly named or rename them accordingly
            # Example:
            # df.columns = ['Column1', 'Column2', 'Column3', 'Column4', 'Event Date']

            dataframes.append(df)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading {file}: {e}")
            continue

    if dataframes:
        try:
            master_dataframe = pd.concat(dataframes, ignore_index=True)
            # Convert the 'Event Date' column to datetime if it's not already in that format
            # Assuming 'Event Date' is in the fifth column, otherwise adjust the index.
            master_dataframe['Date'] = pd.to_datetime(master_dataframe.iloc[:, 4], errors='coerce')
            
            update_loaded_files_label(file_paths)
            update_dropdowns()
        except Exception as e:
            messagebox.showerror("Error", f"Error processing data: {e}")
    else:
        messagebox.showinfo("Info", "No valid data to process.")


    master_dataframe = pd.concat(dataframes, ignore_index=True)
    master_dataframe['Date'] = pd.to_datetime(master_dataframe['Date'])
    update_loaded_files_label(file_paths)
    update_dropdowns()

def update_loaded_files_label(file_paths):
    # Clear the current list
    files_listbox.delete(0, tk.END)

    # Find the longest file name for width adjustment
    max_file_name_length = 0

    # Add base file names to the list
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        files_listbox.insert(tk.END, file_name)
        max_file_name_length = max(max_file_name_length, len(file_name))

    # Adjust the width of the Listbox
    files_listbox.config(width=max_file_name_length)

def update_dropdowns():
    if 'Name' in master_dataframe:
        unique_names = master_dataframe['Name'].dropna().unique()
        name_dropdown['values'] = list(unique_names)
    # Extract all exercise columns except 'Name', 'Birth Date', and 'Event Date'
    exercise_columns = [col for col in master_dataframe.columns if col not in ['Name', 'DOB', 'Date', 'Age']]
    exercise_dropdown['values'] = exercise_columns
    analysis_dropdown['values'] = ['Performance Over Time', 'Performance Comparison', 'Scatter Plot with Highlight']
    analysis_dropdown.set('') 


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
    individual_data = data[data['Name'] == individual_name].sort_values('Date')
    plt.scatter(individual_data['Date'], individual_data[exercise])
    plt.title(f'Performance Over Time for {individual_name} in {exercise}')
    plt.xlabel('Date')
    plt.ylabel(exercise)
    plt.show()
# Declare analysis_dropdown as global
global analysis_dropdown

# ... [Rest of your code] ...

def plot_scatter_with_highlight(data, exercise, individual_name, highlight_color='#ff0000'):
    plt.figure(figsize=(10, 6))
    
    # Default color for other individuals
    default_color = '#00cc99'  # You can choose a different color

    # Plot a single point for the legend label for "Others"
    plt.scatter([], [], color=default_color, label='Others')

    # Plot data for all individuals in default color
    for name in data['Name'].unique():
        if name != individual_name:
            individual_data = data[data['Name'] == name]
            plt.scatter(individual_data['Date'], individual_data[exercise], color=default_color, label='_nolegend_')

    # Highlight the selected individual
    individual_data = data[data['Name'] == individual_name]
    plt.scatter(individual_data['Date'], individual_data[exercise], color=highlight_color, label=individual_name)

    plt.xlabel('Event Date')
    plt.ylabel(exercise)
    plt.title(f'Performance Over Time of {individual_name} vs Others')
    plt.legend()
    plt.show()
    plt.show()

def update_plot():
    selected_name = name_var.get()
    selected_exercise = exercise_var.get()
    analysis_type = analysis_var.get()

    if not selected_name or not selected_exercise:
        messagebox.showwarning("Warning", "Please select a valid name and exercise.")
        return

    if analysis_type == 'Performance Over Time':
        plot_individual_performance_over_time(master_dataframe, selected_name, selected_exercise)
    elif analysis_type == 'Performance Comparison':
        plot_performance_comparison(master_dataframe, selected_exercise, selected_name)
    elif analysis_type == 'Scatter Plot with Highlight':  # Make sure the option matches what's in the dropdown
        plot_scatter_with_highlight(master_dataframe, selected_exercise, selected_name, highlight_color)



def display_dataframe():
    # Check if the DataFrame exists and is not empty
    if 'master_dataframe' not in globals() or master_dataframe.empty:
        messagebox.showerror("Error", "No data has been loaded yet. Please load data first.")
        return

    # Create a new window
    data_window = tk.Toplevel(root)
    data_window.title("Data View")

    # Adjust window width based on the number of columns
    window_width = min(len(master_dataframe.columns) * 100, root.winfo_screenwidth())
    data_window.geometry(f"{window_width}x600")

    # Treeview Widget
    tree_frame = ttk.Frame(data_window)
    tree_frame.pack(pady=10, fill='both', expand=True)

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", columns=list(master_dataframe.columns), show="headings")
    tree.pack(fill='both', expand=True)

    tree_scroll.config(command=tree.yview)

    # Create headings and set column width
    for column in master_dataframe.columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)

    # Populate rows
    df_rows = master_dataframe.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)


# ... [rest of your Tkinter UI code] ...

# ... [rest of your Tkinter UI code] ...

# Create the main window

root = tk.Tk()
root.title("Athlete Performance Analysis")
root.geometry("600x600")

# Define a custom color scheme
background_color = "#4e4e4e"  # Grey background
text_color = "#ffffff"       # White text
button_color = "#000000"     # Black for buttons
button_text_color = "#ffffff" # White text for buttons
hover_color = "#005f8b"
active_color = "#005f8b"
listbox_color = "#333333"    # Darker grey for listbox

# Set a theme and configure style
# Set a theme and configure style
# Set a theme and configure style
style = ttk.Style(root)
style.theme_use('clam')

# General style configuration for the entire app
style.configure('.', font=('Helvetica', 12), background=background_color, foreground=text_color)

# Specific style configuration for Labels
style.configure('TLabel', background=background_color, foreground=text_color)

# Specific style configuration for Buttons
style.configure('TButton', background=button_color, foreground=button_text_color, borderwidth=1)
style.map('TButton',
          background=[('active', active_color), ('pressed', active_color), ('!disabled', button_color)],
          foreground=[('active', button_text_color), ('pressed', text_color), ('!disabled', button_text_color)],
          bordercolor=[('!disabled', button_color)],
          lightcolor=[('!disabled', button_color)],
          darkcolor=[('!disabled', button_color)])

# Specific style configuration for Comboboxes with white background
style.configure('TCombobox', fieldbackground='white', foreground='black', background='white')
style.map('TCombobox',
          fieldbackground=[('!disabled', 'white'), ('active', 'white')],
          background=[('!disabled', 'white'), ('active', 'white')],
          foreground=[('!disabled', 'black'), ('active', 'black')])

# Specific style configuration for Scrollbars
style.configure('Vertical.TScrollbar', background=button_color)
style.configure('Horizontal.TScrollbar', background=button_color)
style.configure('Title.TLabel', font=('Helvetica', 30, 'bold'), background=background_color, foreground='#ffffff')
# Specific style configuration for Treeview (The data table)
style.configure('Treeview', background=listbox_color, fieldbackground=listbox_color, foreground=text_color)
style.map('Treeview', background=[('selected', active_color)])


# Configure the root window's background
root.configure(bg=background_color)

# Title Label
title_label = ttk.Label(root, text="Athlete Stats", style='Title.TLabel')
title_label.pack(pady=20)

# Button to load files
load_button = ttk.Button(root, text="Load CSV/Excel Files", command=load_files)
load_button.pack(pady=10)




# Listbox and Scrollbar for displaying loaded files
files_frame = ttk.Frame(root)
files_frame.pack(pady=10)

# Vertical Scrollbar
files_scroll = ttk.Scrollbar(files_frame)
files_scroll.pack(side="right", fill="y")

# Listbox for displaying loaded files
files_listbox = tk.Listbox(files_frame, yscrollcommand=files_scroll.set, height=4)
files_listbox.pack(side="left", fill='y')

files_scroll.config(command=files_listbox.yview)

# Button to display DataFrame
view_data_button = ttk.Button(root, text="View Data", command=display_dataframe)
view_data_button.pack(pady=10)




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

color_button = ttk.Button(root, text="Choose Highlight Color", command=choose_color)
color_button.pack(pady=10)
highlight_color = '#ff0000'

# Run the application
root.mainloop()
