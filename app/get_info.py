import subprocess
import re

from typing import List
from loguru import logger
from cpuinfo import get_cpu_info


def cpu_info() -> str:
    """
    Get information of cpu
    """
    cpu_info = get_cpu_info()
    cpu = f"{cpu_info['brand_raw']} {cpu_info['count']} core"
    return cpu


def memory_info(sudo: bool = False) -> List:
    """
    Get information of memory
    """
    cmd = ["lshw", "-c", "memory"]
    if sudo:
        cmd.insert(0, "sudo")
    output = subprocess.check_output(cmd)
    decoded_output = output.decode()

    lines = [i for i in decoded_output.split("*-") if i[:4] == "bank"]
    memories = []

    for line in lines:
        pattern_description = re.compile(r"description: (.+)\n")
        pattern_size = re.compile(r"size: (.+)\n")

        description = pattern_description.search(line).group(1) if pattern_description.search(line) else None
        if not description or "empty" in description:
            continue
        size = pattern_size.search(line).group(1) if pattern_size.search(line) else None

        memories.append(f"{description} {size}")

    return memories


def disk_info(sudo: bool = False) -> List:
    """
    Get information of disk
    """
    cmd = ["lshw", "-c", "disk"]
    if sudo:
        cmd.insert(0, "sudo")
    output = subprocess.check_output(cmd)
    decoded_output = output.decode()

    lines = [i for i in decoded_output.split("*-") if i.strip()]
    disks = []

    for line in lines:
        pattern_description = re.compile(r"description: (.+)\n")
        pattern_product = re.compile(r"product: (.+)\n")
        pattern_capacity = re.compile(r"capacity: (.+)\n")
        pattern_size = re.compile(r"size: (.+)\n")

        description = pattern_description.search(line).group(1) if pattern_description.search(line) else None
        product = pattern_product.search(line).group(1) if pattern_product.search(line) else None
        capacity = pattern_capacity.search(line).group(1) if pattern_capacity.search(line) else None
        size = pattern_size.search(line).group(1) if pattern_size.search(line) else None

        disk = f"[{description}]"
        if product:
            disk += f" {product}"
        if capacity:
            disk += f" {capacity}"
        elif size:
            disk += f" {size}"
        disks.append(disk)

    return disks


def network_info(sudo: bool = False) -> List:
    """
    Get information of network
    """
    cmd = ["lshw", "-c", "network"]
    if sudo:
        cmd.insert(0, "sudo")
    output = subprocess.check_output(cmd)
    decoded_output = output.decode()

    lines = [i for i in decoded_output.split("*-") if i.strip()]
    networks = []

    for line in lines:
        pattern_product = re.compile(r"product: (.+)\n")

        product = pattern_product.search(line).group(1) if pattern_product.search(line) else None

        if product and not product in networks:
            networks.append(f"{product}")

    return networks


def hca_info() -> List:
    """
    Get information of hca
    """
    output = subprocess.check_output(["ibstat"])
    decoded_output = output.decode()

    lines = [i for i in decoded_output.split("CA ") if i.strip()]
    hcas = []

    for idx, line in enumerate(lines[::2]):
        hca = line.strip("'\n\t")
        info = lines[idx * 2 + 1]
        if "State: Active" in info and "Physical state: LinkUp" in info and "Link layer: InfiniBand" in info:
            hcas.append(hca)

    return hcas
