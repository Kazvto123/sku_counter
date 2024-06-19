import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Create the main application window
root = tk.Tk()
root.title("SKU COUNTER")

# Create a label
label = tk.Label(root, text="Enter something:")
label.pack(pady=10)

# Create a textbox (Entry widget)
textbox = tk.Entry(root, width=40)
textbox.pack(pady=10)

# Create a frame for the canvas and scrollbar
frame = tk.Frame(root)
frame.pack(pady=10, fill='both', expand=True, side='left')

# Create a canvas widget
canvas = tk.Canvas(frame)
canvas.pack(side='left', fill='both', expand=True)

# Add a scrollbar to the canvas
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side='right', fill='y')

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas to hold the input labels and buttons
input_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=input_frame, anchor='nw')

# Dictionary to store inputs and their counts
input_counts = {}

# List to store input history with timestamps
input_history = []

# Function to update the display of inputs and their counts
def update_display():
    # Clear the current display
    for widget in input_frame.winfo_children():
        widget.destroy()
    
    # Display each input and its count with buttons
    for key, count in input_counts.items():
        row_frame = tk.Frame(input_frame)
        row_frame.pack(fill='x', pady=2)

        input_text = tk.Text(row_frame, height=1, width=40)
        input_text.insert(tk.END, f"{key}: {count}")
        input_text.config(state=tk.DISABLED)  # Make it read-only
        input_text.pack(side='left', padx=5)

        increment_button = tk.Button(row_frame, text="+", command=lambda k=key: modify_count(k, 1))
        increment_button.pack(side='right', padx=5)

        decrement_button = tk.Button(row_frame, text="-", command=lambda k=key: modify_count(k, -1))
        decrement_button.pack(side='right', padx=5)

    # Update the scroll region to include the new widgets
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to update the history display
def update_history():
    history_listbox.delete(0, tk.END)
    for entry in reversed(input_history):
        history_listbox.insert(0, entry)

# Function to be called when the Enter key is pressed
def on_enter_pressed(event):
    user_input = textbox.get().strip()
    
    if user_input:
        # Update the count in the dictionary
        if user_input in input_counts:
            input_counts[user_input] += 1
        else:
            input_counts[user_input] = 1
        
        # Add entry to history with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        input_history.insert(0, f"{timestamp}: {user_input}")  # Insert at the beginning
        
        # Update the displays
        update_display()
        update_history()
        
        # Clear the textbox
        textbox.delete(0, tk.END)

# Function to modify the count of a given input
def modify_count(key, delta):
    if key in input_counts:
        input_counts[key] += delta
        # Remove the key if the count drops to zero
        if input_counts[key] <= 0:
            del input_counts[key]
        update_display()

# Function to export the input_counts to a text file
def export_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            for key, count in input_counts.items():
                file.write(f"{key}: {count}\n")

# Bind the Enter key to the function
textbox.bind('<Return>', on_enter_pressed)

# Create a frame for the history tab
history_frame = tk.Frame(root)
history_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

# Label for the history tab
history_label = tk.Label(history_frame, text="Input History")
history_label.pack(pady=10)

# Listbox to display history with scrollbar
history_listbox = tk.Listbox(history_frame, width=50, height=20)
history_listbox.pack(fill='both', expand=True)

# Scrollbar for the history listbox
history_scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=history_listbox.yview)
history_scrollbar.pack(side='right', fill='y')

# Configure the listbox to use the scrollbar
history_listbox.configure(yscrollcommand=history_scrollbar.set)

# Export button
export_button = tk.Button(history_frame, text="Export Data", command=export_to_file)
export_button.pack(pady=10)

# Run the application
root.mainloop()
