#!/usr/bin/env python3

import time

def create_cpu_plot(fig_cpu, ax_cpu, timestamps, system_data, user_data, start_time):
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

def create_gpu_plot(fig_gpu, ax_gpu, timestamps, gpu_data, start_time):
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
