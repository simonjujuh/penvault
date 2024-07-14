from pathlib import Path
from penvault import config
from penvault.model import Vault, VaultsManager


# Completion methods
# --archive
def complete_all_vaults():
    # List of containers from filesystem
    return VaultsManager()._refresh_list(mounted_only=False)

# --close
def complete_opened_vaults():
    print(VaultsManager()._refresh_list(mounted_only=True))
    return VaultsManager()._refresh_list(mounted_only=True)

# --open
def complete_closed_vaults():
    all_vaults = VaultsManager()._refresh_list(mounted_only=False)
    opened_vaults = VaultsManager()._refresh_list(mounted_only=True)

    return list(set(all_vaults) - set(opened_vaults))