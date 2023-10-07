#!/usr/bin/env python3

"""
Python 3 - Linux prometheus exporter
"""

__version__="0.1.2"
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

def update_metrics():
    try:
        """
        Metrics update
        """
        cpu_dict = cpu_usage()
        for chave, valor in cpu_dict.items():
            variable_name = "cpu_percent_" + chave
            template = f"CPU {chave} percent"
            vars()[variable_name] = Gauge(variable_name, template)
        while True:
            # Metricas de uso de CPU
            cpu_dict = cpu_usage()
            for chave, valor in cpu_dict.items():
                variable_name = "cpu_percent_" + chave
                vars()[variable_name].set(valor)
            time.sleep(0.1)
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
        update_metrics()
    except Exception as e:
        print('\nExporter Falhou e Foi Finalizado! \n\n======> %s\n' % e)
        exit(1)

if __name__ == '__main__':
    main()
    exit(0)
