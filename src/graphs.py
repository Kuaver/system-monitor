#!/usr/bin/env python3

import time

def length_limiter(start_time):
    elapsed_time = time.time() - start_time
    return (0 if elapsed_time < 30 else elapsed_time - 30, max(elapsed_time, 30))

def create_cpu_plot(fig_cpu, ax_cpu, timestamps, system_data, user_data, start_time):
    ax_cpu.clear()
    xlim_values = length_limiter(start_time)
    ax_cpu.set_xlim(xlim_values)
    ax_cpu.invert_xaxis()
    ax_cpu.set_ylim([None, 100])
    ax_cpu.yaxis.set_label_position("right")
    ax_cpu.yaxis.tick_right()

    ax_cpu.plot(timestamps, system_data, label="System", color="red")
    ax_cpu.plot(timestamps, user_data, label="User", color="blue")
    ax_cpu.legend(loc="upper left", bbox_to_anchor=(0, 1))

def create_gpu_plot(fig_gpu, ax_gpu, timestamps, gpu_data, start_time):
    ax_gpu.clear()

    xlim_values = length_limiter(start_time)
    ax_gpu.set_xlim(xlim_values)
    ax_gpu.set_ylim([None, 100])

    ax_gpu.plot(timestamps, gpu_data, label="GPU", color="green")
    ax_gpu.legend(loc="upper right", bbox_to_anchor=(1, 1))
