import tkinter as tk
from tkinter import filedialog

def open_file():
    root = tk.Tk()
    root.withdraw()  # hide the root window
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        print(f"Selected file: {file_path}")

# create a button that triggers the open_file function
button = tk.Button(text="Open", command=open_file)
button.pack()

# start the Tkinter event loop
tk.mainloop()