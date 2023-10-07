#!/usr/bin/env python3

"""
Python 3 - System monitor
"""

__version__="0.1.1"
__author__="Gabriel Hespnhol"

import psutil
import os
import requests
import json
import time
from prometheus_client import start_http_server, Gauge


def memory_ram():
    return dict(psutil.virtual_memory()._asdict())

def cpu_usage():
    return dict(psutil.cpu_times_percent(interval=0.5)._asdict())

def update_linux_metrics():
    try:
        """
        Atualiza as métricas
        """
        cpu_percent_user = Gauge('cpu_percent_user', 'CPU user percent')
        cpu_percent_nice = Gauge('cpu_percent_nice', 'CPU nice percent')
        cpu_percent_system = Gauge('cpu_percent_system', 'CPU system percent')
        cpu_percent_idle = Gauge('cpu_percent_idle', 'CPU idle percent')
        cpu_percent_iowait = Gauge('cpu_percent_iowait', 'CPU iowait percent')
        memoria_ram_total = Gauge('ram_memory_total', 'RAM Total')
        while True:
            # Metricas de uso de CPU
            cpu_percent_user.set(cpu_usage()['user'])
            cpu_percent_nice.set(cpu_usage()['nice'])
            cpu_percent_system.set(cpu_usage()['system'])
            cpu_percent_idle.set(cpu_usage()['idle'])
            cpu_percent_iowait.set(cpu_usage()['iowait'])
            # Metricas de uso de RAM
            memoria_ram_total.set(memory_ram()['total'])
            time.sleep(5)
    except Exception as e:
        print("Problemas para atualizar as métricas! \n\n====> %s \n" % e)
        raise e

def start_exporter():
    try:
        """
        Iniciar o exporter
        """
        start_http_server(8899)
        return True
    except Exception as e:
        print("O Servidor não pode ser iniciado!")
        raise e


def main():
    try:
        start_exporter()
        print('Exporter Iniciado')
        update_linux_metrics()
    except Exception as e:
        print('\nExporter Falhou e Foi Finalizado! \n\n======> %s\n' % e)
        exit(1)

if __name__ == '__main__':
    main()
    exit(0)
