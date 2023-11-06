#!/usr/bin/env python3

"""
Python 3 - Linux prometheus exporter
"""

__version__="0.1.4"
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

# Get swap memory usage
def get_swap():
    return dict(psutil.swap_memory()._asdict())

# Get network info
def get_network_inf():
    return dict(psutil.net_io_counters()._asdict())

# Get cpu cores total
def cpu_core_count():
    return str(os.cpu_count())

# Get system uptime
def get_system_uptime():
    return str(time.time() - psutil.boot_time())

# Set variable names and metrics
def update_metrics():
    try:
        """
        Metrics update
        """
        cpu_dict = get_cpu_usage()
        cpu_count = cpu_core_count()
        memory_dict = get_memory_ram()
        disk_dict = get_disk_usage()
        swap_dict = get_swap()
        network_dict = get_network_inf()
        system_uptime = get_system_uptime()
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
        # Looping set description in swap metrics
        for key, value in swap_dict.items():
            variable_name = "swap_" + key
            template = f"Swap {key}"
            vars()[variable_name] = Gauge(variable_name, template)
        # Looping set description in network metrics
        for key, value in network_dict.items():
            variable_name = "network_" + key
            template = f"Network {key}"
            vars()[variable_name] = Gauge(variable_name, template)
        # Set cpu cores count metrics
        if len(cpu_count) > 0:
            variable_name = "cpu_count_cores"
            template = "CPU Cores"
            vars()[variable_name] = Gauge(variable_name, template)
        # Set uptime metric
        uptime_system = Gauge("uptime_system", "Uptime do systema")
        while True:
            # Metricas de uso de CPU
            cpu_dict = get_cpu_usage()
            cpu_count = cpu_core_count()
            memory_dict = get_memory_ram()
            disk_dict = get_disk_usage()
            swap_dict = get_swap()
            network_dict = get_network_inf()
            system_uptime = get_system_uptime()
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
            # Set metrics swap memory
            for key, value in swap_dict.items():
                variable_name = "swap_" + key
                vars()[variable_name].set(value)
            # Set metrics network
            for key, value in network_dict.items():
                variable_name = "network_" + key
                vars()[variable_name].set(value)
            # Set CPU core count metrics
            if len(cpu_count) > 0:
                variable_name = "cpu_count_cores"
                vars()[variable_name].set(cpu_count)
            # Set uptime metric
            uptime_system.set(get_system_uptime())
            time.sleep(0.2)
    except Exception as e:
        print("Metrics update ERROR")
        raise e

# Funcao para iniciar o exporter
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