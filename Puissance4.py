import tkinter as tk
from tkinter import messagebox

# Constantes
WIDTH = 700
HEIGHT = 600


# Variables globales
root = None

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

    
def main():
    global root
    root = tk.Tk()
    root.title("Puissance 4")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.mainloop()
    
print("")
print('')
