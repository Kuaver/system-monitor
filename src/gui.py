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

def create_top_frame(window):
    top_frame = tk.Frame(window, padx=10, pady=10)
    top_frame.pack(side=tk.TOP)
    top_frame.columnconfigure(0, weight=0)
    top_frame.columnconfigure(0, weight=0)
    return top_frame

def create_cpu_label(top_frame):
    cpu_label = tk.Label(top_frame, text="", font=("Arial", 12), width=65, justify="left", anchor="w")
    cpu_label.grid(column=0, row=0)
    return cpu_label

def create_gpu_label(top_frame):
    gpu_label = tk.Label(top_frame, text="", font=("Arial", 12), width=45, justify="left", anchor="w")
    gpu_label.grid(column=1, row=0)
    return gpu_label

def create_main_frame(window):
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(side=tk.BOTTOM)
    main_frame.columnconfigure(0, weight=0)
    main_frame.columnconfigure(0, weight=0)
    return main_frame

def create_cpu_canvas(fig_cpu, main_frame):
    canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=main_frame)
    canvas_cpu.draw()
    canvas_cpu.get_tk_widget().pack(side=tk.LEFT, expand=False)
    return canvas_cpu

def create_gpu_canvas(fig_gpu, main_frame):
    canvas_gpu = FigureCanvasTkAgg(fig_gpu, master=main_frame)
    canvas_gpu.draw()
    canvas_gpu.get_tk_widget().pack(side=tk.RIGHT, expand=False)
    return canvas_gpu
