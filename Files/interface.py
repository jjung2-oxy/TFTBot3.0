import tkinter as tk
from tkinter import Toplevel, Label
import re
import sys

curr_list = []

def get_curr_list():
    return curr_list

def strip_parentheses(name):
    # Find the position of the opening parenthesis
    pos = name.find('(')
    if pos != -1:
        # Strip everything from the opening parenthesis onwards
        return name[:pos].strip()
    else:
        return name.strip()
def on_button_toggle(line, button_var):
    def toggle():
        try: 
            stripped_line = strip_parentheses(line)
            if button_var.get():
                # Button is pressed, add to the list
                if stripped_line not in curr_list:
                    curr_list.append(stripped_line)
            else:
                # Button is unpressed, remove from the list
                if stripped_line in curr_list:
                    curr_list.remove(stripped_line)
        except Exception as e:
            print(f"Error in toggle: {e}", file=sys.stderr)
    return toggle


def create_tooltip(widget, text):
    def on_enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        # Create a toplevel window
        global tooltip_window
        tooltip_window = Toplevel(widget)
        tooltip_window.wm_overrideredirect(True)
        tooltip_window.wm_geometry(f"+{x}+{y}")
        label = Label(tooltip_window, text=text, justify='left',
                      background='#ffffff', relief='solid', borderwidth=1,
                      font=("times", "8", "normal"))
        label.pack(ipadx=1)
    def on_leave(event):
        tooltip_window.destroy()
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def interface():
    # Create the main window
    root = tk.Tk()
    root.title("Tkinter Dynamic Button Layout")

    # Read lines from a text file
    with open("./Files/set10_champs.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    # Variables to control the layout
    button_height = 2  # Approximate height of each button
    button_width = 20  # Fixed width of each button in characters
    text_height = 1    # Height of the textbox
    row_height = 40    # Estimated pixel height per row (button + textbox)
    max_rows_per_column = 30  # Maximum number of rows per column

    # Calculate the required number of columns and rows
    num_lines = len(lines)
    num_columns = (num_lines // max_rows_per_column) + (1 if num_lines % max_rows_per_column else 0)
    num_rows = min(num_lines, max_rows_per_column)

    # Calculate window size
    window_width = num_columns * (button_width * 8)  # 8 pixels per character width approx
    window_height = num_rows * row_height

    root.geometry(f"{window_width * 2}x{window_height - window_width}")

    current_row = 0
    current_column = 0

    # Create a button and a textbox for each line
    for line in lines:
        if line.endswith(":" or line == ""):
            current_row = 0
            current_column += 1
            # Create a label as a column header
            header = tk.Label(root, text=line, font=("Helvetica", 12, "bold"))
            header.grid(row=current_row, column=current_column, sticky="nsew")
            current_row += 1
            continue

        # Extract text in parentheses
        parenthetical_text = re.search(r'\((.*?)\)', line)
        if parenthetical_text:
            parenthetical_text = parenthetical_text.group(1)
        else:
            parenthetical_text = ""

        # Create checkbutton
        button_var = tk.BooleanVar()
        button = tk.Checkbutton(root, text=line.split('(')[0][:button_width], 
                                indicatoron=False, selectcolor="light grey", 
                                var=button_var, command=on_button_toggle(line, button_var), 
                                relief="raised")
        button.grid(row=current_row, column=current_column, sticky="nsew")

        create_tooltip(button, line)

        # Create textbox
        textbox = tk.Text(root, height=text_height, width=button_width)
        textbox.grid(row=current_row + 1, column=current_column, sticky="nsew")
        textbox.insert(tk.END, parenthetical_text)
        textbox.config(state=tk.DISABLED)

        current_row += 2  # Increment by 2 to account for the textbox
        # if current_row >= max_rows_per_column:
        #     current_row = 0
        #     current_column += 1

    # Adjust column weights so they expand equally
    for col in range(current_column + 1):
        root.grid_columnconfigure(col, weight=1)

    def clear_curr_list():
        curr_list.clear()
        print("curr_list cleared:", curr_list)

    # Create a 'Clear' button
    clear_button = tk.Button(root, text="Clear", command=clear_curr_list)
    # Place the 'Clear' button at the bottom center
    # Adjust the row and column span if needed
    clear_button.grid(row=num_rows * 2, column=num_columns // 2, sticky="nsew")
    # Start the GUI event loop

    return root
