import os
import time

from datetime import datetime
from loguru import logger
from kubernetes import client, config

from get_info import *


# Get node name
node_name = os.environ.get("MY_NODE_NAME")

# Load kubernetes config
cfg = config.load_incluster_config()
logger.info("Load kubernetes config")

# Create kubernetes client
k8s_client = client.ApiClient(cfg)
logger.info("Create kubernetes client")

# Create kubernetes v1
v1 = client.CoreV1Api(k8s_client)
logger.info("Create kubernetes v1")

# Get hardware information
hardware_info = {
    "updated_datetime": datetime.now().isoformat(),
    "cpu": cpu_info(),
    "memory": memory_info(),
    "disk": disk_info(),
    "network": network_info(),
}
logger.info(f"Get hardware information: node_name={node_name}, hardware_info={hardware_info}")

# Get node annotations
node = v1.read_node(name=node_name)

# Cast to string for input annotations, Replace single quote for reading with json.loads()
hardware_info = str(hardware_info).replace("'", '"')
node.metadata.annotations["hardware-info"] = hardware_info

# Patch node annotations
v1.patch_node(name=node_name, body=node)
logger.info(f"Path node annotations: node_name={node_name}, hardware_info={hardware_info}")
