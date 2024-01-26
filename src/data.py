#!/usr/bin/env python3

import numpy as np
import psutil
import cpuinfo
import GPUtil

CPU_NAME = f"{cpuinfo.get_cpu_info()['brand_raw']}"

def cpu_utilization(user_data, system_data, idle_data):
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

    return f"""{CPU_NAME}
            User: {user_utilization:.1f}% (Avg: {user_avg:.1f}%, Peak: {user_peak:.1f}%)
            System: {system_utilization:.1f}% (Avg: {system_avg:.1f}%, Peak: {system_peak:.1f}%)
            Idle: {idle_utilization:.1f}% (Avg: {idle_avg:.1f}%, Peak: {idle_peak:.1f}%)"""


def gpu_utilization(gpu_data):
    gpus = GPUtil.getGPUs()
    gpu_utilizations = [gpu.load * 100 for gpu in gpus]
    gpu_names = [gpu.name for gpu in gpus]
    gpu_avg = np.mean(gpu_data) if len(gpu_data) > 0 else 0
    gpu_peak = np.max(gpu_data) if len(gpu_data) > 0 else 0

    return f"""{gpu_names[0]}
            Utilization: {gpu_utilizations[0]:.1f}% (Avg: {gpu_avg:.1f}%, Peak: {gpu_peak:.1f}%)"""
