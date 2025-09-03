import tkinter as tk
from tkinter import messagebox

def hello():
    messagebox.showinfo("Hello", "Tombol ditekan!")

root = tk.Tk()
root.title("Test Button")
root.geometry("250x150")

btn = tk.Button(root, text="Klik Aku!", command=hello)
btn.pack(pady=40)

root.mainloop()
