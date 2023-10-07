#!/usr/bin/env python3

"""
Python 3 - Linux prometheus exporter
"""

__version__="0.1.3"
__author__="Gabriel Hespnhol"

import psutil
import os
import requests
import json
import time
from prometheus_client import start_http_server, Gauge

# Get memory ram infos
def get_memory_ram():
    return dict(psutil.virtual_memory()._asdict())

# Get cpu usage info
def get_cpu_usage():
    return dict(psutil.cpu_times_percent(interval=0.5)._asdict())

# Get principal disk usage info
def get_disk_usage():
    return dict(psutil.disk_usage(path="/")._asdict())

# Set variable names and metrics
def update_metrics():
    try:
        """
        Metrics update
        """
        cpu_dict = get_cpu_usage()
        memory_dict = get_memory_ram()
        disk_dict = get_disk_usage()
        # Looping set description in cpu metrics
        for key, value in cpu_dict.items():
            variable_name = "cpu_percent_" + key
            template = f"CPU {key} percent"
            vars()[variable_name] = Gauge(variable_name, template)
        # Looping set description in memory ram rescription
        for key, value in memory_dict.items():
            variable_name = "ram_memory_" + key
            template = f"RAM memory {key}"
            vars()[variable_name] = Gauge(variable_name, template)
        # Looping set description in disk rescription
        for key, value in disk_dict.items():
            variable_name = "disk_" + key
            template = f"Disk {key}"
            vars()[variable_name] = Gauge(variable_name, template)
        while True:
            # Metricas de uso de CPU
            cpu_dict = get_cpu_usage()
            memory_dict = get_memory_ram()
            disk_dict = get_disk_usage()
            # set metrics variable CPU
            for key, value in cpu_dict.items():
                variable_name = "cpu_percent_" + key
                vars()[variable_name].set(value)
            # set metrics variable RAM
            for key, value in memory_dict.items():
                variable_name = "ram_memory_" + key
                vars()[variable_name].set(value)
            # set metrics variable disk
            for key, value in disk_dict.items():
                variable_name = "disk_" + key
                vars()[variable_name].set(value)
            time.sleep(0.1)
    except Exception as e:
        print("Metrics update ERROR")
        raise e

def start_exporter():
    try:
        """
        Exporter running
        """
        start_http_server(8899)
        return True
    except Exception as e:
        print("Exporter server start ERROR")
        raise e


def main():
    try:
        start_exporter()
        print('Exporter is running')
        update_metrics()
    except Exception as e:
        print('\n Exporter start error')
        exit(1)

if __name__ == '__main__':
    main()
    exit(0)
