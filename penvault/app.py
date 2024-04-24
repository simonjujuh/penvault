
###
import sys
from penvault.first_run import first_run_setup

from penvault.config import containers_path, mount_path
from penvault.cli import build_cli_args
from penvault.logger import log


def main():
    first_run_setup()
    args = build_cli_args()
    

if __name__ == '__main__':
    main()
    sys.exit(0)

# class Config(object):

#     def __init__(self,)


# class VaultController(object):

#     # Private methods
#     def __init__(self) -> None:
#         pass
#     def _vault_to_container(self, vault_name):
#         """
#         """
#         return self._veracrypt_container_path / Path(vault_name).with_suffix('.vc')

#     def _container_to_vault(self, container_name):
#         """
#         """
#         return str(Path(container_name).name)[:-3]

#     # Public methods
#     def show_app_config(self):
#         log.info(f"config file is       : {self._config_file_path}")
#         log.info(f"veracrypt containers : {self._veracrypt_container_path}")
#         log.info(f"veracrypt mount path : {self._veracrypt_mount_path}")

#     def create_vault(self, vault_name, vault_size, auto_mount=False):
#         # Get the vault name
#         container_path = Path(self._vault_to_container(vault_name))

#         # Generate random password
#         length = 30
#         characters = string.ascii_letters + string.digits + string.punctuation
#         password = ''.join(secrets.choice(characters) for _ in range(length))

#         # Do not overwrite an existing container
#         if container_path.exists():
#             log.error(f"{container_path.name} already exists, please use another vault name")
#             sys.exit(1)

#         # Create a container
#         try:
#             veracrypt.create_container(container_path, vault_size, password)
#             log.success(f"{container_path.name} created successfully with password {password}")
#         except Exception as e:
#             log.error(f"unable to create {container_path}: {e}")
#             sys.exit(1)
#         except KeyboardInterrupt:
#             pass
#         finally:
#             if auto_mount:
#                 self.open_vault(vault_name)

#     def open_vault(self, vault_name):
#         # Get the vault name
#         container_path = Path(self._vault_to_container(vault_name))

#         # Check if container path exists
#         if not container_path.exists():
#             log.error(f"{container_path} does not exist, exiting.")
#             sys.exit(1)

#         # Check if veracrypt mount path exists
#         if not self._veracrypt_mount_path.exists():
#             log.error(f"{self._veracrypt_mount_path} mount point does not exist, exiting.")
#             sys.exit(1)
        
#         # Mount container
#         directory_path = self._veracrypt_mount_path / vault_name

#         # Creating the directory if it doesn't exist
#         try:
#             directory_path.mkdir(parents=False, exist_ok=True)
#             veracrypt.mount_container(container_path, directory_path, '') # empty password means it will be prompted
#             log.success(f"{container_path.name} mounted: {directory_path}")
#         except Exception as e:
#             log.error(f"unable to mount {container_path}: {e}")
#             sys.exit(1)
#         except KeyboardInterrupt:
#             directory_path.rmdir()

#     def list_vaults(self):
#         """
#         """
#         # Fetch the mounted container list
#         mounted_containers = veracrypt.list_mounted_containers()

#         # Get .vc containers from the filesystem
#         # Use a regular expression to filter VeraCrypt files
#         veracrypt_fs_containers = [str(e) for e in self._veracrypt_container_path.glob("*.vc*")]
#         veracrypt_fs_containers.sort()

#         for container in mounted_containers:
#             # vault = self._container_to_vault(container['path'])
#             # print(f"{vault.ljust(35)} {container['mount point']}")
#             veracrypt_fs_containers.remove(container['path'])
        
#         dismounted_containers = []
#         for container in veracrypt_fs_containers:
#             vault = self._container_to_vault(container)
#             dismounted_containers.append(vault)

#         log.info("list of dismounted containers")
#         [log.success(container) for container in dismounted_containers]
        
#         print() # newline
#         log.info("list of mounted containers")
#         for container in mounted_containers:
#             vault = self._container_to_vault(container['path'])
#             log.success(f"{vault} at {container['mount point']}")

#     def prune_vaults(self):
#         # Get the current date
#         current_date = datetime.datetime.now()
#         no_delete = True

#         # Iterate over files in the directory
#         for container in self._veracrypt_container_path.iterdir():
#             # Check if it's a file
#             if container.is_file():
#                 # Get the file's creation time
#                 creation_time = datetime.datetime.fromtimestamp(container.stat().st_ctime)
#                 # Calculate the difference in days
#                 difference = (current_date - creation_time).days
#                 # Check if the file is older than one year
#                 if difference > 365:
#                     # Ask for confirmation
#                     # confirmation = input(f"Do you want to delete {file_path.name}? (Yes/No) ").lower()
#                     # if confirmation == 'yes':
#                     #     # Delete the file
#                     #     file_path.unlink()
#                     #     print(f"{file_path.name} successfully deleted.")
#                     log.warning(f'{container.name} is older than a year')
#                     no_delete = False
        
#         if no_delete:
#             log.info(f'No containers ready for deletion')



#     def close_vault(self, vault_name):
#         container_path = self._vault_to_container(vault_name)

#         # Check if container is mounted or not
#         mounted_containers = [entry['path'] for entry in veracrypt.list_mounted_containers()]
#         if not str(container_path) in mounted_containers:
#             log.error(f"{container_path.name} not mounted, exiting")
#             sys.exit(1)

#         try:
#             veracrypt.umount_container(container_path)
#             log.success(f"{container_path.name} unmounted successfully")
#         except Exception as e:
#             log.error(f"unable to dismount '{container_path.name}': {e}")
#             sys.exit(1)
#         except KeyboardInterrupt:
#             pass
#         else:
#             directory_path = self._veracrypt_mount_path / vault_name
#             if directory_path.exists():
#                 directory_path.rmdir()

#     # Completion methods
#     def complete_all_vaults(self, prefix, parsed_args, **kwargs):
#         # List of containers from filesystem
#         veracrypt_fs_containers = []

#         # Get all .vc files from veracrypt container path and add it to the list
#         for container in self._veracrypt_container_path.glob("*.vc*"):
#             vault = self._container_to_vault(container) # convert veracrypt to vault
#             veracrypt_fs_containers.append(vault)

#         # Build the completion tuple
#         complete_vaults = (vault for vault in veracrypt_fs_containers if vault.startswith(prefix))

#         # Return sorted tuple
#         return tuple(sorted(complete_vaults))
    
#     def complete_opened_vaults(self, prefix, parsed_args, **kwargs):
#         opened_vaults = []
#         # Get the mounted containers
#         mounted_containers = veracrypt.list_mounted_containers()

#         # Build the liste of opened vaults
#         for container in mounted_containers:
#             opened_vaults.append(self._container_to_vault(container['path']))
        
#         # Build the completion tuple
#         complete_vaults = (vault for vault in opened_vaults if vault.startswith(prefix))
        
#         # Return sorted tuple
#         return tuple(sorted(complete_vaults))
