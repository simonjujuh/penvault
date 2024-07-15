from pathlib import Path
from penvault import config
from penvault.model import VaultsManager, Vault

containers_info = VaultsManager().get_containers_dict()

# Completion methods
# --archive
def complete_all_vaults():
    vaults = [container for container in containers_info.keys()]
    vaults.sort()
    return vaults

# --close
def complete_opened_vaults():
    vaults = [container_name for container_name, container_info in containers_info.items() if container_info is not None]
    vaults.sort()
    return vaults

# --open
def complete_closed_vaults():
    vaults = [container_name for container_name, container_info in containers_info.items() if container_info is None]
    vaults.sort()
    return vaults

