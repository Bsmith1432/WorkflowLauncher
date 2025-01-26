import webbrowser
import json
from tkinter import *

# File path to save button data
DATA_FILE = 'buttons_data.json'


# Function to open a URL
def open_url(url):
    webbrowser.open_new_tab(url)


# Function to add a new button
def add_button():
    url = url_entry.get()
    button_text = button_entry.get()
    if url and button_text:  # Ensure both URL and button text are provided
        # Add new button data to the list
        button_data.append((button_text, url))

        # Create the new button dynamically
        total_buttons = len(buttons)
        row = total_buttons // 2
        col = total_buttons % 2  # 0 for left, 1 for right

        new_button = Button(button_frame, text=button_text, font=('Perpetua', 16, 'bold'),
                            bg='#00a3e0', fg='white', activebackground='white',
                            activeforeground='#00a3e0', width=20, height=2)
        new_button.config(command=lambda: open_url(url))  # Set the button to open the URL
        new_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        buttons.append(new_button)  # Add the button to the list for tracking

        # Add the new button to the Listbox for deletion
        button_listbox.insert(END, button_text)

        # Clear the input fields
        url_entry.delete(0, END)
        button_entry.delete(0, END)

        # Re-center all buttons after adding a new one
        for i in range(len(buttons)):  # Re-center buttons
            button_frame.grid_rowconfigure(i, weight=1, uniform="equal")
            button_frame.grid_columnconfigure(0, weight=1, uniform="equal")
            button_frame.grid_columnconfigure(1, weight=1, uniform="equal")

        # Save the button data to the file
        save_buttons()


# Function to delete the selected button
def delete_button():
    selected_index = button_listbox.curselection()
    if selected_index:
        # Get the button text to delete
        button_text = button_listbox.get(selected_index)

        # Find the button with the matching text and remove it from the grid and list
        for btn in buttons:
            if btn.cget("text") == button_text:
                btn.grid_forget()  # Remove button from the grid
                buttons.remove(btn)  # Remove from the buttons list
                break

        # Remove the button from the Listbox
        button_listbox.delete(selected_index)

        # Remove the button data from the list
        global button_data
        button_data = [data for data in button_data if data[0] != button_text]

        # Save the updated button data to the JSON file
        save_buttons()


# Function to save button data to a JSON file
def save_buttons():
    with open(DATA_FILE, 'w') as file:
        json.dump(button_data, file)


# Function to load button data from a JSON file
def load_buttons():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist


# Window setup
window = Tk()
window.geometry('600x700')
window.title('Workflow Optimizer')
window.config(bg="#c5c5c4")
window.resizable(False, False)

# Frames for better alignment
button_frame = Frame(window, bg="#c5c5c4")
button_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

input_frame = Frame(window, bg="#c5c5c4")
input_frame.pack(side=BOTTOM, fill=X, padx=20, pady=10)  # Position at the bottom

# Empty list for buttons and button data
buttons = []
button_data = load_buttons()

# Create buttons based on the loaded data
for text, url in button_data:
    total_buttons = len(buttons)
    row = total_buttons // 2
    col = total_buttons % 2  # 0 for left, 1 for right

    new_button = Button(button_frame, text=text, font=('Perpetua', 16, 'bold'),
                        bg='#00a3e0', fg='white', activebackground='white',
                        activeforeground='#00a3e0', width=20, height=2)
    new_button.config(command=lambda url=url: open_url(url))  # Set the button to open the URL
    new_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    buttons.append(new_button)  # Add the button to the list for tracking

# Initialize Listbox for Deletion
button_listbox = Listbox(input_frame, height=4, width=30, font=('Perpetua', 12))
button_listbox.grid(row=1, column=2, rowspan=2, padx=5)

# Update the Listbox for Deleting
for text, _ in button_data:
    button_listbox.insert(END, text)

# Configure grid weights for button_frame
for i in range(5):  # Rows (set an arbitrary number for flexibility)
    button_frame.grid_rowconfigure(i, weight=1, uniform="equal")
for i in range(2):  # Columns (set to 2 for left and right)
    button_frame.grid_columnconfigure(i, weight=1, uniform="equal")

# Input Section for Adding Buttons (Centered in the bottom frame)
Label(input_frame, text="Add New Button:", font=('Perpetua', 14, 'bold'), bg='#c5c5c4').grid(row=0, column=0,
                                                                                             columnspan=2, pady=5)

Label(input_frame, text="Button Text:", font=('Perpetua', 12), bg='#c5c5c4').grid(row=1, column=0, sticky=E, padx=5)
button_entry = Entry(input_frame, width=30)
button_entry.grid(row=1, column=1, padx=5)

Label(input_frame, text="URL:", font=('Perpetua', 12), bg='#c5c5c4').grid(row=2, column=0, sticky=E, padx=5)
url_entry = Entry(input_frame, width=30)
url_entry.grid(row=2, column=1, padx=5)

add_button_btn = Button(input_frame, text="Add Button", font=('Perpetua', 14, 'bold'),
                        bg='#00a3e0', fg='white', activebackground='white',
                        activeforeground='#00a3e0', command=add_button)
add_button_btn.grid(row=3, column=0, pady=10)

# Delete Button Section
Label(input_frame, text="Select Button to Delete:", font=('Perpetua', 14, 'bold'), bg='#c5c5c4').grid(row=0, column=2,
                                                                                                      padx=5)

delete_button_btn = Button(input_frame, text="Delete Button", font=('Perpetua', 14, 'bold'),
                           bg='#e64a19', fg='white', activebackground='white',
                           activeforeground='#e64a19', command=delete_button)
delete_button_btn.grid(row=3, column=2, pady=10)

# Main Loop
window.mainloop()
