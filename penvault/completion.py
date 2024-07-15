from pathlib import Path
from penvault import config
from penvault.model import VaultsManager, Vault

containers_info = VaultsManager().get_containers_dict()

# Completion methods
# --archive
def complete_all_vaults():
    return [container for container in containers_info.keys()]

# --close
def complete_opened_vaults():
    return [container_name for container_name, container_info in containers_info.items() if container_info is not None]
    # return VaultsManager()._refresh_list(mounted_only=True)

# --open
def complete_closed_vaults():
    return [container_name for container_name, container_info in containers_info.items() if container_info is None]
