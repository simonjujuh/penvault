import sys
from penvault.config import containers_path, mount_path
from penvault.cli import build_cli_args
from penvault.logger import log
from penvault.model import ContainersManager, Vault

def main():
    args = build_cli_args()
    
    # Create instances
    manager = ContainersManager()


    # penvault.py --auto-mount --create <VAULT> --size <SIZE> --template <NAME>
    if args.create:
        if not args.size:
            log.error("The --size option is required when --create is selected")
            sys.exit(1)
        else:
            vault = Vault(args.create)
            vault.create(args.size, auto_mount=args.auto_mount)
    
    # penvault.py --open <VAULT>
    elif args.open:
        # open accept mutliple vaults
        for vault in args.open:
            pass

    # penvault.py --resize <VAULT>
    elif args.resize:
        # resize accept mutliple vaults
        for vault in args.resize:
            pass

    # penvault.py --close <VAULT>
    elif args.close:
        # close accept mutliple vaults
        for vault in args.close:
            pass

    # Available containers:
    # 01: vault 1 </path/>
    # 02: vault 2
    # 03: vault 3
    # 04: vault 4 </path/>
    elif args.list: 
        manager.list()
    elif args.prune:
        pass

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




#     def list_vaults(self):
#         """
#         """


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
