#!/usr/bin/env python3

"""
Python 3 - System monitor
"""

__version__="0.1.0"
__author__="Gabriel Hespnhol"

import psutil
import os

def memory_ram():
    return dict(psutil.virtual_memory()._asdict())

def cpu_usage():
    return dict(psutil.cpu_times_percent(interval=0.5)._asdict())

def resultado(ram_memory, uso_cpu):
    for chave, valor in ram_memory.items():
        print(f"RAM {chave}= {valor}")
    for chave, valor in uso_cpu.items():
        print(f"CPU {chave}= {valor}")


def main():
    uso_cpu = cpu_usage()
    ram_memory = memory_ram()
    resultado(ram_memory, uso_cpu)

if __name__ == '__main__':
    main()
    exit(0)
