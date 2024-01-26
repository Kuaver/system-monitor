#!/usr/bin/env python3

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import psutil
import cpuinfo
from datetime import datetime

CPU_NAME = f"{cpuinfo.get_cpu_info()['brand_raw']}"

def cpu_utilization():
    cpu_times = psutil.cpu_times_percent()
    user_utilization = cpu_times.user
    system_utilization = cpu_times.system
    idle_utilization = cpu_times.idle

    # Calculate averages and peaks
    user_avg = np.mean(user_data) if len(user_data) > 0 else 0
    system_avg = np.mean(system_data) if len(system_data) > 0 else 0
    idle_avg = np.mean(idle_data) if len(idle_data) > 0 else 0
    user_peak = np.max(user_data) if len(user_data) > 0 else 0
    system_peak = np.max(system_data) if len(system_data) > 0 else 0
    idle_peak = np.min(idle_data) if len(idle_data) > 0 else 0

    return f"{CPU_NAME}\nUser: {user_utilization:.1f}% (Avg: {user_avg:.1f}%, Peak: {user_peak:.1f}%)\nSystem: {system_utilization:.1f}% (Avg: {system_avg:.1f}%, Peak: {system_peak:.1f}%)\nIdle: {idle_utilization:.1f}% (Avg: {idle_avg:.1f}%, Peak: {idle_peak:.1f}%)"

# Initialize data arrays
system_data = np.array([])
user_data = np.array([])
idle_data = np.array([])
timestamps = np.array([])

# Create a Tkinter window
window = tk.Tk()
window.title('System and User CPU Utilization')
window.geometry('800x600')

# Create a Tkinter Label to display the CPU information
cpu_label = tk.Label(window, text='', font=('Arial', 12))
cpu_label.pack(side=tk.TOP, pady=10)

# Create a Tkinter Frame to hold the legend
legend_frame = tk.Frame(window)
legend_frame.pack(side=tk.BOTTOM, padx=20, pady=(0, 20))

# Create a Figure and Axes for the plot
fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('CPU Utilization (%)')

# Create a Tkinter Canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Start gathering and plotting data
start_time = time.time()
while True:
    # Get CPU utilization
    utilization = cpu_utilization()
    utilization_lines = utilization.split('\n')
    user_utilization = float(utilization_lines[1].split(':')[1].split('%')[0].strip().replace(',', '.'))
    system_utilization = float(utilization_lines[2].split(':')[1].split('%')[0].strip().replace(',', '.'))
    idle_utilization = float(utilization_lines[3].split(':')[1].split('%')[0].strip().replace(',', '.'))

    # Append data to arrays
    system_data = np.append(system_data, system_utilization)
    user_data = np.append(user_data, user_utilization)
    idle_data = np.append(idle_data, idle_utilization)
    timestamps = np.append(timestamps, time.time() - start_time)

    # Clear the plot
    ax.clear()

    # Plot system utilization
    ax.plot(timestamps, system_data, label='System', color='red')

    # Plot user utilization
    ax.plot(timestamps, user_data, label='User', color='blue')

    # Add legend to the legend frame
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1))

    # Update the plot
    canvas.draw()

    # Update the CPU label with the latest data
    system_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cpu_label.config(text=f"Time: {system_time}\n{utilization}")

    # Update the Tkinter window
    window.update()

    # Pause for a short duration
    time.sleep(0.1)

# Start the Tkinter event loop
window.mainloop()
