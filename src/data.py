#!/usr/bin/env python3

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import psutil
import cpuinfo
import GPUtil
from datetime import datetime

CPU_NAME = f"{cpuinfo.get_cpu_info()['brand_raw']}"


def cpu_utilization():
    cpu_times = psutil.cpu_times_percent()
    user_utilization = cpu_times.user
    system_utilization = cpu_times.system
    idle_utilization = cpu_times.idle

    # Calculate averages and peaks
    user_avg = np.mean(user_data[-174:]) if len(user_data) > 0 else 0
    system_avg = np.mean(system_data[-174:]) if len(system_data) > 0 else 0
    idle_avg = np.mean(idle_data[-174:]) if len(idle_data) > 0 else 0
    user_peak = np.max(user_data[-174:]) if len(user_data) > 0 else 0
    system_peak = np.max(system_data[-174:]) if len(system_data) > 0 else 0
    idle_peak = np.min(idle_data[-174:]) if len(idle_data) > 0 else 0

    return f"""{CPU_NAME}
            User: {user_utilization:.1f}% (Avg: {user_avg:.1f}%, Peak: {user_peak:.1f}%)
            System: {system_utilization:.1f}% (Avg: {system_avg:.1f}%, Peak: {system_peak:.1f}%)
            Idle: {idle_utilization:.1f}% (Avg: {idle_avg:.1f}%, Peak: {idle_peak:.1f}%)"""


def gpu_utilization():
    gpus = GPUtil.getGPUs()
    gpu_utilizations = [gpu.load * 100 for gpu in gpus]
    gpu_names = [gpu.name for gpu in gpus]
    gpu_avg = np.mean(gpu_data[-174:]) if len(gpu_data) > 0 else 0
    gpu_peak = np.max(gpu_data[-174:]) if len(gpu_data) > 0 else 0

    return f"""{gpu_names[0]}
            Utilization: {gpu_utilizations[0]:.1f}% (Avg: {gpu_avg:.1f}%, Peak: {gpu_peak:.1f}%)"""


def on_close():
    window.quit()
    window.destroy()


# Initialize data arrays
system_data = np.array([])
user_data = np.array([])
idle_data = np.array([])
gpu_data = np.array([])
timestamps = np.array([])

# Create a Tkinter window
window = tk.Tk()
window.title("System and User CPU Utilization")
window.geometry("1200x600")
window.protocol("WM_DELETE_WINDOW", on_close)
window.resizable(width=False, height=False)

# Create a Tkinter Frame to hold the top part of the panel
top_frame = tk.Frame(window, padx=10, pady=10)
top_frame.pack(side=tk.TOP)
top_frame.columnconfigure(0, weight=0)
top_frame.columnconfigure(0, weight=0)

# Create a Tkinter Label to display the CPU information
cpu_label = tk.Label(top_frame, text="", font=("Arial", 12), width=60)
cpu_label.grid(column=0, row=0)

# Create a Tkinter Label to display the GPU information
gpu_label = tk.Label(top_frame, text="", font=("Arial", 12), width=60)
gpu_label.grid(column=1, row=0)

# Create a Figure and Axes for the CPU plot
fig_cpu, ax_cpu = plt.subplots()
fig_cpu.set_figwidth(6)

# Create a Figure and Axes for the GPU plot
fig_gpu, ax_gpu = plt.subplots()
fig_gpu.set_figwidth(6)

# Create a Tkinter Frame to hold the main part of the panel
main_frame = tk.Frame(window, padx=10, pady=10)
main_frame.pack(side=tk.BOTTOM)
main_frame.columnconfigure(0, weight=0)
main_frame.columnconfigure(0, weight=0)

# Create a Tkinter Canvas to display the CPU plot
canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=main_frame)
canvas_cpu.draw()
canvas_cpu.get_tk_widget().pack(side=tk.LEFT, expand=False)

# Create a Tkinter Canvas to display the GPU plot
canvas_gpu = FigureCanvasTkAgg(fig_gpu, master=main_frame)
canvas_gpu.draw()
canvas_gpu.get_tk_widget().pack(side=tk.RIGHT, expand=False)

# Start gathering and plotting data
start_time = time.time()
while True:
    # Get CPU utilization
    cpu_utilization_data = cpu_utilization()
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
    gpu_utilization_data = gpu_utilization()
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

    # Clear the CPU plot
    ax_cpu.clear()

    ax_cpu.set_xlim(
        [
            0 if time.time() - start_time < 30 else time.time() - start_time - 30,
            max(time.time() - start_time, 30),
        ]
    )
    ax_cpu.invert_xaxis()
    ax_cpu.set_ylim([None, 100])
    ax_cpu.yaxis.set_label_position("right")
    ax_cpu.yaxis.tick_right()

    # Plot system utilization
    ax_cpu.plot(timestamps, system_data, label="System", color="red")

    # Plot user utilization
    ax_cpu.plot(timestamps, user_data, label="User", color="blue")

    # Add legend to the CPU plot
    ax_cpu.legend(loc="upper left", bbox_to_anchor=(0, 1))

    # Update the CPU plot
    canvas_cpu.draw()

    # Clear the GPU plot
    ax_gpu.clear()

    ax_gpu.set_xlim(
        [
            0 if time.time() - start_time < 30 else time.time() - start_time - 30,
            max(time.time() - start_time, 30),
        ]
    )
    ax_gpu.set_ylim([None, 100])

    # Plot GPU utilization
    ax_gpu.plot(timestamps, gpu_data, label="GPU", color="green")

    # Add legend to the GPU plot
    ax_gpu.legend(loc="upper right", bbox_to_anchor=(1, 1))

    # Update the GPU plot
    canvas_gpu.draw()

    # Update the CPU label with the latest data
    cpu_label.config(text=f"{cpu_utilization_data}")

    # Update the GPU label with the latest data
    gpu_label.config(text=f"{gpu_utilization_data}")

    # Update the Tkinter window
    window.update()
    
    print(f"{len(gpu_data)} at {time.time() - start_time} seconds") # Debug purposes

    # Pause for a short duration
    time.sleep(0.1)
