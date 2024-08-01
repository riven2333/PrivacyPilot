# -*- encoding: utf-8 -*-
'''
@File    :   disk.py
@Time    :   2024/07/13 22:05:53
@Contact :   small_dark@sina.com
@Brief   :   local plugin for disk usage
'''

import psutil

def get_disk_usage(path='/'):
    usage = psutil.disk_usage(path)
    total_gb = usage.total / (1024 ** 3)
    used_gb = usage.used / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)
    percent_used = usage.percent

    disk_usage = {
        'total_gb': total_gb,
        'used_gb': used_gb,
        'free_gb': free_gb,
        'percent_used': percent_used
    }
    
    print(f"Total: {disk_usage['total_gb']:.2f} GB")
    print(f"Used: {disk_usage['used_gb']:.2f} GB")
    print(f"Free: {disk_usage['free_gb']:.2f} GB")
    print(f"Percent Used: {disk_usage['percent_used']}%")

    return disk_usage

