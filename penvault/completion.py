from penvault.model import Vault, VaultsManager

# Completion methods
def complete_all_vaults(prefix, parsed_args, **kwargs):
    # List of containers from filesystem
    veracrypt_fs_containers = []

    # Get all .vc files from veracrypt container path and add it to the list
    for container in config.containers_path.glob("*.vc*"):
        vault = Vault('').from_container(container) # convert veracrypt to vault
        veracrypt_fs_containers.append(vault)

    # Build the completion tuple
    complete_vaults = (vault for vault in veracrypt_fs_containers if vault.startswith(prefix))

    # Return sorted tuple
    return tuple(sorted(complete_vaults))


def complete_opened_vaults(prefix, parsed_args, **kwargs):
    opened_vaults = []
    # Get the mounted containers
    mounted_containers = VaultsManager()._refresh_list(mounted_only=True)

    # Build the liste of opened vaults
    for vc_path in mounted_containers.keys:
        vc_path = Path(vc_path)
        v = Vault('').from_container(vc_path)
        opened_vaults.append(v.name)
    
    # Build the completion tuple
    complete_vaults = (vault for vault in opened_vaults if vault.startswith(prefix))
    
    # Return sorted tuple
    return tuple(sorted(complete_vaults))
