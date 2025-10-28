import tkinter as tk
from tkinter import filedialog
import os
import re

class FindingForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Finder")

        # Create a label and textbox for searching
        tk.Label(self.root, text="Search:").grid(row=0, column=0)
        self.pattern_textbox = tk.Entry(self.root, width=20, font=("MS Gothic", 12))
        self.pattern_textbox.grid(row=0, column=1)

        # Create a button to search
        tk.Button(self.root, text="Search", command=self.search_files).grid(row=0, column=2)

        # Create a button to browse folder
        tk.Button(self.root, text="Browse", command=self.browse_folder).grid(row=0, column=3)

        # Create a label for selected folder
        self.folder_label = tk.Label(self.root, text="")
        self.folder_label.grid(row=1, column=1)

        # Create a Listbox to display the search results
        self.result_listbox = tk.Listbox(self.root, width=60, font=("MS Gothic", 12), selectmode=tk.EXTENDED)
        self.result_listbox.grid(row=2, column=0, columnspan=4)

        # Create a button to open the selected files
        tk.Button(self.root, text="Open Selected Files", command=self.open_selected_files).grid(row=3, column=0)

        # Create a button to rename the selected files
        self.rename_button = tk.Button(self.root, text="Rename", command=self.rename_files)
        self.rename_button.grid(row=3, column=3)

        # Bind the "Enter" key to the search button
        self.root.bind("<Return>", lambda event: self.search_button.invoke())

        # Create a search button to bind the "Enter" key to
        self.search_button = tk.Button(self.root, text="Search", command=self.search_files)
        self.search_button.grid_forget()

        self.root.mainloop()
    def browse_folder(self):
        # Open file dialog to select a folder
        folder_path = filedialog.askdirectory()
        self.folder_label.config(text=folder_path)

    def search_files(self):
        # Get the input pattern from the textbox
        pattern = self.pattern_textbox.get()
        if not pattern:
            self.result_listbox.delete(0, tk.END)
            self.file_paths = []
            return

        # Get the selected folder path
        folder_path = self.folder_label.cget("text")
        if not folder_path:
            return

        # Convert the pattern to a regular expression
        pattern = pattern.replace("*", ".*").replace(".", "\.")

        # Search for files that match the pattern
        self.result_listbox.delete(0, tk.END)
        self.file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if re.match(pattern, file, re.UNICODE):
                    self.result_listbox.insert(tk.END, file)
                    self.file_paths.append(os.path.join(root, file))

    def open_selected_files(self):
        # Get the selected indices
        indices = self.result_listbox.curselection()

        # Open the selected files
        for index in indices:
            file_path = self.file_paths[index]
            os.startfile(file_path)
    def rename_files(self):
        # Get the selected indices
        indices = self.result_listbox.curselection()

        # Create a new form to rename files
        rename_form = tk.Toplevel(self.root)
        rename_form.title("Rename Files")

        # Create a label and textbox for new file name
        tk.Label(rename_form, text="New File Name:").grid(row=0, column=0)
        new_name_textbox = tk.Entry(rename_form, width=50, font=("MS Gothic", 12))
        new_name_textbox.grid(row=0, column=1)

        # Create radio buttons for replace and change
        tk.Label(rename_form, text="Rename Mode:").grid(row=1, column=0)
        rename_mode = tk.StringVar()
        rename_mode.set("replace")  # default value
        tk.Radiobutton(rename_form, text="New", variable=rename_mode, value="replace", command=lambda: enable_disable_change_mode(False)).grid(row=1, column=1)
        tk.Radiobutton(rename_form, text="Change", variable=rename_mode, value="change", command=lambda: enable_disable_change_mode(True)).grid(row=1, column=2)

        # Create radio buttons for prefix and postfix
        tk.Label(rename_form, text="Change Mode:").grid(row=2, column=0)
        change_mode = tk.StringVar()
        change_mode.set("prefix")  # default value
        prefix_button = tk.Radiobutton(rename_form, text="Prefix", variable=change_mode, value="prefix", state=tk.DISABLED)
        prefix_button.grid(row=2, column=1)
        postfix_button = tk.Radiobutton(rename_form, text="Postfix", variable=change_mode, value="postfix", state=tk.DISABLED)
        postfix_button.grid(row=2, column=2)

        def enable_disable_change_mode(enable):
            prefix_button.config(state=tk.NORMAL if enable else tk.DISABLED)
            postfix_button.config(state=tk.NORMAL if enable else tk.DISABLED)

        # Create a button to rename files
        tk.Button(rename_form, text="Rename", command=lambda: self.rename_files_with_name(new_name_textbox.get(), indices, rename_mode.get(), change_mode.get())).grid(row=3, column=1)
    def rename_files_with_name(self, new_name, indices, rename_mode, change_mode):
        # Sort the selected file names
        file_names = [self.file_paths[index] for index in indices]
        file_names.sort()

        # Rename the selected files
        for i, file_path in enumerate(file_names):
            file_name, file_ext = os.path.splitext(file_path)
            if rename_mode == "replace":
                new_file_name = f"{new_name}{file_ext}"
            else:
                if change_mode == "prefix":
                    new_file_name = f"{new_name}-{i+1}{file_name}{file_ext}"
                else:
                    new_file_name = f"{file_name}{new_name}-{i+1}{file_ext}"
            os.rename(file_path, new_file_name)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    form = FindingForm()
    form.run()