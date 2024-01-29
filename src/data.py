#!/usr/bin/env python3

import numpy as np
import psutil
import cpuinfo
import GPUtil

CPU_NAME = f"{cpuinfo.get_cpu_info()['brand_raw']}"

def calculate_avg_peak(*data_sets, increments_per_thirty_seconds):
    last_thirty_seconds_data = [data[-increments_per_thirty_seconds:] for data in data_sets]
    return {i: (np.mean(data), np.max(data)) if len(data) > 0 else (0, 0) for i, data in enumerate(last_thirty_seconds_data)}


def cpu_utilization(user_data, system_data, idle_data, increments_per_thirty_seconds):
    cpu_times = psutil.cpu_times_percent()
    avgs_peaks = calculate_avg_peak(user_data, system_data, idle_data, increments_per_thirty_seconds = increments_per_thirty_seconds)

    return f"""{CPU_NAME}
            User: {cpu_times.user:.1f}% (Avg: {avgs_peaks[0][0]:.1f}%, Peak: {avgs_peaks[0][1]:.1f}%)
            System: {cpu_times.system:.1f}% (Avg: {avgs_peaks[1][0]:.1f}%, Peak: {avgs_peaks[1][1]:.1f}%)
            Idle: {cpu_times.idle:.1f}% (Avg: {avgs_peaks[2][0]:.1f}%, Peak: {avgs_peaks[2][1]:.1f}%)"""

def gpu_utilization(gpu_data, increments_per_thirty_seconds):
    gpus = GPUtil.getGPUs()
    gpu_utilizations = [gpu.load * 100 for gpu in gpus]
    gpu_names = [gpu.name for gpu in gpus]
    gpu_avg, gpu_peak = calculate_avg_peak(gpu_data, increments_per_thirty_seconds = increments_per_thirty_seconds).get(0, (0, 0))

    return f"""{gpu_names[0]}
            Utilization: {gpu_utilizations[0]:.1f}% (Avg: {gpu_avg:.1f}%, Peak: {gpu_peak:.1f}%)"""
