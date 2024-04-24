import sys
import string, secrets
import shutil
import datetime
from pathlib import Path
from penvault import veracrypt
from penvault.logger import log
from penvault.config import cfg

class Vault(object):

    def __init__(self, name=''):
        self.name = name

    # container will be a PosixPath
    def to_container(self):
        # Convert vault like "myvault" to "/path/to/containers/myvault.vc"
        # Returns a Path Object
        return Path(Config.veracrypt_containers_path / Path(self.name).with_suffix('.vc'))

    def from_container(self, container):
        # Convert container like "/path/to/containers/container.vc" to "container"
        name = Path(container).name[:-3]
        return Vault(str(name))


# class Controller(object):

#     # Private methods
#     def __init__(self) -> None:
#         self.config = Config()
#         self.veracrypt_containers_path = Path(self.config['veracrypt']['']) # Path
#         self.veracrypt_mount_point     = None # Path

#     def list_vaults(self):
#         # Fetch the mounted container list
#         mounted_containers = veracrypt.list_mounted_containers()

#         # Get .vc containers from the filesystem
#         # Use a regular expression to filter VeraCrypt files
#         veracrypt_fs_containers = [str(e) for e in self.veracrypt_containers_path.glob("*.vc*")]
#         veracrypt_fs_containers.sort()

#         log.info("vaults list")
#         # container is a str here
#         for container in veracrypt_fs_containers:
#             # Convert container to vault
#             vault = Vault().from_container(container)
#             # The veracrypt container is in the mounted containers list
#             if container in mounted_containers.keys():
#                 mount_point = mount_container.get(container)
#                 log.warning(f"{vault.ljust(35)} mounted at: {mount_point}")
#             else:
#                 log.success(f"{vault}")

#     def create_vault(self, vault_name, vault_size, auto_mount=False):
#         # Convert vault to container path
#         container = Vault(vault_name).to_container()

#         # Generate random password
#         length = 30
#         characters = string.ascii_letters + string.digits + string.punctuation
#         password = ''.join(secrets.choice(characters) for _ in range(length))

#         # Do not overwrite an existing container
#         if container.exists():
#             log.error(f"{container.name} already exists, please use another vault name")
#             sys.exit(1)

#         # Create a container
#         try:
#             veracrypt.create_container(container, vault_size, password)
#             log.success(f"{container.name} created successfully with password {password}")
#         except Exception as e:
#             log.error(f"unable to create {container}: {e}")
#             sys.exit(1)
#         except KeyboardInterrupt:
#             pass
#         finally:
#             if auto_mount:
#                 self.open_vault(vault_name)

#     def open_vault(self, vault_name):
#         # Get the vault name
#         container = Vault(vault_name).to_container()

#         # Check if container path exists
#         if not container.exists():
#             log.error(f"{container} does not exist, exiting.")
#             sys.exit(1)

#         # Check if veracrypt mount path exists
#         if not self.veracrypt_mount_point.exists():
#             log.error(f"{self.veracrypt_mount_point} mount point does not exist, exiting.")
#             sys.exit(1)
        
#         # Mount container
#         vault_directory = self.veracrypt_mount_point / vault_name

#         # Creating the directory if it doesn't exist
#         try:
#             vault_directory.mkdir(parents=False, exist_ok=True)
#             veracrypt.mount_container(container, vault_directory, '') # empty password means it will be prompted
#             log.success(f"{container.name} mounted: {vault_directory}")
#         except Exception as e:
#             log.error(f"unable to mount {container}: {e}")
#             sys.exit(1)
#         except KeyboardInterrupt:
#             vault_directory.rmdir()

#     def close_vault(self, vault_name):
#         # Container is Path object
#         container = Vault(vault_name).to_container() 

#         # Check if container is mounted or not
#         mounted_containers = veracrypt.list_mounted_containers()

#         if str(container) not in mounted_containers.keys():
#             log.error(f"{container.name} not mounted, exiting")
#             sys.exit(1)



#         try:
#             veracrypt.umount_container(container)
#             log.success(f"{container.name} unmounted successfully")
#         except Exception as e:
#             log.error(f"unable to dismount '{container.name}': {e}")
#             sys.exit(1)
#         except KeyboardInterrupt:
#             pass
#         else:
#             directory_path = self._veracrypt_mount_point / vault_name
#             if directory_path.exists():
#                 directory_path.rmdir()

# ####################################################################""







#     # def prune_vaults(self):
#     #     # Get the current date
#     #     current_date = datetime.datetime.now()
#     #     no_delete = True

#     #     # Iterate over files in the directory
#     #     for container in self._veracrypt_containers_path.iterdir():
#     #         # Check if it's a file
#     #         if container.is_file():
#     #             # Get the file's creation time
#     #             creation_time = datetime.datetime.fromtimestamp(container.stat().st_ctime)
#     #             # Calculate the difference in days
#     #             difference = (current_date - creation_time).days
#     #             # Check if the file is older than one year
#     #             if difference > 365:
#     #                 # Ask for confirmation
#     #                 # confirmation = input(f"Do you want to delete {file_path.name}? (Yes/No) ").lower()
#     #                 # if confirmation == 'yes':
#     #                 #     # Delete the file
#     #                 #     file_path.unlink()
#     #                 #     print(f"{file_path.name} successfully deleted.")
#     #                 log.warning(f'{container.name} is older than a year')
#     #                 no_delete = False
        
#     #     if no_delete:
#     #         log.info(f'No containers ready for deletion')

#     # def resize_vault(self, vault_name):
#     #     # Check if vault is opened
#     #     # Compute the directory size
#     #     # Create a temp vault with optimal size, and auto open
#     #     # Move content from big vault to resized vault
#     #     # Close the vault
#     #     # Delete the vault 

#     # # Completion methods
#     # def complete_all_vaults(self, prefix, parsed_args, **kwargs):
#     #     # List of containers from filesystem
#     #     veracrypt_fs_containers = []

#     #     # Get all .vc files from veracrypt container path and add it to the list
#     #     for container in self._veracrypt_containers_path.glob("*.vc*"):
#     #         vault = self._container_to_vault(container) # convert veracrypt to vault
#     #         veracrypt_fs_containers.append(vault)

#     #     # Build the completion tuple
#     #     complete_vaults = (vault for vault in veracrypt_fs_containers if vault.startswith(prefix))

#     #     # Return sorted tuple
#     #     return tuple(sorted(complete_vaults))
    
#     # def complete_opened_vaults(self, prefix, parsed_args, **kwargs):
#     #     opened_vaults = []
#     #     # Get the mounted containers
#     #     mounted_containers = veracrypt.list_mounted_containers()

#     #     # Build the liste of opened vaults
#     #     for container in mounted_containers:
#     #         opened_vaults.append(self._container_to_vault(container['path']))
        
#     #     # Build the completion tuple
#     #     complete_vaults = (vault for vault in opened_vaults if vault.startswith(prefix))
        
#     #     # Return sorted tuple
#     #     return tuple(sorted(complete_vaults))


if __name__ == '__main__':
    print(config)

    # v = Vault('test')
    # # Path object
    # container = v.to_container()
    # # Vault object
    # v.from_container(container)
