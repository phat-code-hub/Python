import tkinter as tk
from tkinter import messagebox
class A(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        self.label = tk.Label(self, text="Hello, Tkinter!",font=("Arial", 16),fg="blue")
        self.label.pack(pady=10)
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Click me!\n(You can click me multiple times)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="Thoat", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
    def say_hi(self):
        messagebox.showinfo("Greeting","Hello everyone!")
        
class B(A):
    def __init__(self,master=None):
        super().__init__(master)
        self.label.config(fg="green")
        self.hi_there.config(command=self.on_button_click)  
    def create_widgets(self):
        super().create_widgets()
        self.label["text"] = "Hello from B!"
        self.label["fg"] = "green"
        self.hi_there["text"] = "Press me!\n(I am from B class)"
    def say_hi(self):
        messagebox.showinfo("Greeting","Hello from B class!")
    def on_button_click(self):
        self.label["text"] = ("Button in B clicked!")

root = tk.Tk()
# app = A(master=root)
# app.mainloop()
app = B(master=root)
app.mainloop()