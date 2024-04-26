from pathlib import Path
from penvault import config
from penvault.model import Vault, VaultsManager


# Completion methods
def complete_all_vaults():
    # List of containers from filesystem
    veracrypt_fs_containers = []

    # Get all .vc files from veracrypt container path and add it to the list
    for container in config.containers_path.glob("*.vc*"):
        vault = Vault('').from_container(container) # convert veracrypt to vault
        veracrypt_fs_containers.append(vault.name)

    veracrypt_fs_containers.sort()
    return veracrypt_fs_containers


def complete_opened_vaults():
    opened_vaults = []
    # Get the mounted containers
    mounted_containers = VaultsManager()._refresh_list(mounted_only=True)
    
    # Build the liste of opened vaults
    for vc_path in mounted_containers.keys():
        vc_path = Path(vc_path)
        v = Vault('').from_container(vc_path)
        opened_vaults.append(v.name)
    
    opened_vaults.sort()
    return opened_vaults


def complete_closed_vaults():
    all_vaults = complete_all_vaults()
    opened_vaults = complete_opened_vaults()

    return list(set(all_vaults) - set(opened_vaults))