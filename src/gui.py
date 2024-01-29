#!/usr/bin/env python3

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_window(on_close):
    window = tk.Tk()
    window.title("System and User CPU Utilization")
    window.geometry("1200x600")
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.resizable(width=False, height=False)
    return window

def create_frame(window, side, padx=10, pady=10):
    frame = tk.Frame(window, padx=padx, pady=pady)
    frame.pack(side=side)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(0, weight=0)
    return frame

def create_label(frame, width, column, row):
    label = tk.Label(frame, text="", font=("Arial", 12), width=width, justify="left", anchor="w")
    label.grid(column=column, row=row)
    return label

def create_canvas(fig, frame, side):
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=side, expand=False)
    return canvas
