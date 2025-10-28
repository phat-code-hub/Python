import tkinter as tk

class A(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.label = tk.Label(self, text="Ready", fg="blue", font=("Arial", 14))
        self.label.pack()
        self.button = tk.Button(self, text="Run")
        self.button.pack()


class B:
    def __init__(self, form: A):
        self.form = form
        # Connect event handler to A's button
        self.form.button.config(command=self.on_button_click)

    def on_button_click(self):
        self.form.label.config(text="Running...", fg="green")


root = tk.Tk()
ui = A(master=root)
controller = B(ui)
root.mainloop()
