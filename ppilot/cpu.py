# -*- encoding: utf-8 -*-
'''
@File    :   cpu.py
@Time    :   2024/07/13 21:29:08
@Contact :   small_dark@sina.com
@Brief   :   local plugin for cpu
'''

import platform
import subprocess

def get_cpu_model():
    system = platform.system()
    if system == "Windows":
        model = platform.processor()
    elif system == "Linux":
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    model = line.split(":")[1].strip()
    elif system == "Darwin":  # macOS
        model = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    else:
        model = "Unsupported platform"
    print("[MODEL]", model)
    return model
    

