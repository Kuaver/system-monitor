#!/usr/bin/env python3

import time
import numpy as np
from data import cpu_utilization, gpu_utilization
from gui import create_window, create_frame, create_label, create_canvas
from graphs import create_cpu_plot, create_gpu_plot
import matplotlib.pyplot as plt
from tkinter import BOTTOM, TOP, LEFT, RIGHT

def on_close():
    window.quit()
    window.destroy()

def parse_utilization_data(utilization_data):
    return float(utilization_data.split(":")[1].split("%")[0].strip().replace(",", "."))

def create_plot_figure():
    fig, ax = plt.subplots()
    fig.set_figwidth(6)
    return fig, ax

def append_data(data_array, new_data):
    return np.append(data_array, new_data)

def update_plots_and_labels(cpu_data, gpu_data, timestamps, start_time):
    create_cpu_plot(fig_cpu, ax_cpu, timestamps, cpu_data['system'], cpu_data['user'], start_time)
    canvas_cpu.draw()
    create_gpu_plot(fig_gpu, ax_gpu, timestamps, gpu_data, start_time)
    canvas_gpu.draw()
    cpu_label.config(text="\n".join(cpu_utilization_data))
    gpu_label.config(text="\n".join(gpu_utilization_data))

# Initialize data arrays
data_arrays = {
    'system': np.array([]),
    'user': np.array([]),
    'idle': np.array([]),
    'gpu': np.array([]),
    'timestamps': np.array([])
}

# Create GUI components
window = create_window(on_close)
main_frame = create_frame(window = window, side = BOTTOM)
top_frame = create_frame(window = window, side = TOP)
cpu_label = create_label(frame = top_frame, width = 65, column = 0, row = 0)
gpu_label = create_label(frame = top_frame, width = 45, column = 1, row = 0)
fig_cpu, ax_cpu = create_plot_figure()
fig_gpu, ax_gpu = create_plot_figure()
canvas_cpu = create_canvas(fig = fig_cpu, frame = main_frame, side = LEFT)
canvas_gpu = create_canvas(fig = fig_gpu, frame = main_frame, side = RIGHT)

# Start gathering and plotting data
start_time = time.time()
loop_times = []
loop_count = 0

while True:
    cpu_utilization_data = cpu_utilization(data_arrays['user'], data_arrays['system'], data_arrays['idle'], increments_per_thirty_seconds = loop_count).split("\n")
    gpu_utilization_data = gpu_utilization(data_arrays['gpu'], increments_per_thirty_seconds = loop_count).split("\n")

    data_arrays['user'] = append_data(data_arrays['user'], parse_utilization_data(cpu_utilization_data[1]))
    data_arrays['system'] = append_data(data_arrays['system'], parse_utilization_data(cpu_utilization_data[2]))
    data_arrays['idle'] = append_data(data_arrays['idle'], parse_utilization_data(cpu_utilization_data[3]))
    data_arrays['gpu'] = append_data(data_arrays['gpu'], parse_utilization_data(gpu_utilization_data[1]))
    data_arrays['timestamps'] = append_data(data_arrays['timestamps'], time.time() - start_time)

    update_plots_and_labels(data_arrays, data_arrays['gpu'], data_arrays['timestamps'], start_time)
    window.update()
    time.sleep(0.1)

    loop_times.append(time.time() - start_time)
    loop_count = len(loop_times)

    loop_times = [t for t in loop_times if t >= loop_times[-1] - 30]

    print("Number of loops in the last 30 seconds:", loop_count)
