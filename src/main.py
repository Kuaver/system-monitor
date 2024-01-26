#!/usr/bin/env python3

import time
import numpy as np
from datetime import datetime
from data import cpu_utilization, gpu_utilization
from gui import create_window, create_top_frame, create_cpu_label, create_gpu_label, create_main_frame, create_cpu_canvas, create_gpu_canvas
from graphs import create_cpu_plot, create_gpu_plot
import matplotlib.pyplot as plt

# Initialize data arrays
system_data = np.array([])
user_data = np.array([])
idle_data = np.array([])
gpu_data = np.array([])
timestamps = np.array([])

length_array = []

def on_close():
    window.quit()
    window.destroy()

# Create a Tkinter window
window = create_window(on_close)

# Create a Tkinter Frame to hold the top part of the panel
top_frame = create_top_frame(window)

# Create a Tkinter Label to display the CPU information
cpu_label = create_cpu_label(top_frame)

# Create a Tkinter Label to display the GPU information
gpu_label = create_gpu_label(top_frame)

# Create a Figure and Axes for the CPU plot
fig_cpu, ax_cpu = plt.subplots()
fig_cpu.set_figwidth(6)

# Create a Figure and Axes for the GPU plot
fig_gpu, ax_gpu = plt.subplots()
fig_gpu.set_figwidth(6)

# Create a Tkinter Frame to hold the main part of the panel
main_frame = create_main_frame(window)

# Create a Tkinter Canvas to display the CPU plot
canvas_cpu = create_cpu_canvas(fig_cpu, main_frame)

# Create a Tkinter Canvas to display the GPU plot
canvas_gpu = create_gpu_canvas(fig_gpu, main_frame)

# Start gathering and plotting data
start_time = time.time()
while True:
    # Get CPU utilization
    cpu_utilization_data = cpu_utilization(user_data, system_data, idle_data)
    cpu_utilization_lines = cpu_utilization_data.split("\n")
    user_utilization = float(
        cpu_utilization_lines[1].split(":")[1].split("%")[0].strip().replace(",", ".")
    )
    system_utilization = float(
        cpu_utilization_lines[2].split(":")[1].split("%")[0].strip().replace(",", ".")
    )
    idle_utilization = float(
        cpu_utilization_lines[3].split(":")[1].split("%")[0].strip().replace(",", ".")
    )

    # Get GPU utilization
    gpu_utilization_data = gpu_utilization(gpu_data)
    gpu_utilization_lines = gpu_utilization_data.split("\n")
    gpu_load = float(
        gpu_utilization_lines[1].split(":")[1].split("%")[0].strip().replace(",", ".")
    )

    # Append data to arrays
    system_data = np.append(system_data, system_utilization)
    user_data = np.append(user_data, user_utilization)
    idle_data = np.append(idle_data, idle_utilization)
    gpu_data = np.append(gpu_data, gpu_load)
    timestamps = np.append(timestamps, time.time() - start_time)

    # Update the CPU plot
    create_cpu_plot(fig_cpu, ax_cpu, timestamps, system_data, user_data, start_time)
    canvas_cpu.draw()

    # Update the GPU plot
    create_gpu_plot(fig_gpu, ax_gpu, timestamps, gpu_data, start_time)
    canvas_gpu.draw()

    # Update the CPU label with the latest data
    cpu_label.config(text=f"{cpu_utilization_data}")

    # Update the GPU label with the latest data
    gpu_label.config(text=f"{gpu_utilization_data}")

    # Update the Tkinter window
    window.update()

    # Pause for a short duration
    time.sleep(0.1)
