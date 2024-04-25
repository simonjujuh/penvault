import sys
import shutil
import subprocess
import string, secrets
import datetime
from pathlib import Path
from penvault import veracrypt
from penvault import config
from penvault.logger import log

class Vault(object):
    
    def __init__(self, name):
        self.name = name
        if self.name.endswith('.vc'):
            raise ValueError("Vault object cannot ends with '.vc'")
    
    def to_container(self):
        return config.containers_path / Path(self.name).with_suffix('.vc')

    def from_container(self, container_path):
        return Vault(container_path.with_suffix('').name)

    def create(self, size, auto_mount=False):
        # Get the vault name
        vc_path = self.to_container()

        # Generate random password
        length = 30
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Do not overwrite an existing container
        if vc_path.exists():
            log.error(f"{vc_path} already exists, please use another vault name")
            sys.exit(1)

        # Create a container
        try:
            veracrypt.create_container(vc_path, size, password)
            log.success(f"{self.name} created successfully with password {password}")
        except Exception as e:
            log.error(f"unable to create {vc_path}: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            pass
        finally:
            if auto_mount:
                pass
                # self.open_vault(vault_name)

    def open(self):
        # Get the vault name
        vc_path = self.to_container()

        # Check if container path exists
        if not vc_path.exists():
            log.error(f"{self.name} does not exist, exiting.")
            sys.exit(1)

        # Check if veracrypt mount path exists
        if not config.mount_path.exists():
            log.error(f"{config.mount_path} mount point does not exist, exiting.")
            sys.exit(1)
        
        # Mount container
        vault_mount_directory = config.mount_path / self.name

        # Creating the directory if it doesn't exist
        try:
            vault_mount_directory.mkdir(parents=False, exist_ok=True)
            veracrypt.mount_container(vc_path, vault_mount_directory, '') # empty password means it will be prompted
            log.success(f"{self.name} mounted: {vault_mount_directory}")
        except Exception as e:
            log.error(f"unable to mount {self.name}: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            vault_mount_directory.rmdir()

    def close(self):
        vc_path = self.to_container()
        print(vc_path)

        # Check if container is mounted or not
        if not self.is_mounted():
            log.error(f"{self.name} not mounted, exiting")
            sys.exit(1)

        try:
            veracrypt.umount_container(vc_path)
            log.success(f"{self.name} unmounted successfully")
        except Exception as e:
            log.error(f"unable to dismount '{self.name}': {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            pass
        else:
            directory_path = config.mount_path / self.name
            if directory_path.exists():
                directory_path.rmdir()

    def is_mounted(self):
        # ...
        vc_path = self.to_container()
        if str(vc_path) in veracrypt.list_mounted_containers():
            return True

        return False


class VaultsManager(object):

    def __init__(self):
        pass

    def _refresh_list(self, mounted_only=False):
        # Get the mounted containers
        output = veracrypt.list_mounted_containers()
        output_lines = output.strip().split('\n')

        containers = {}

        # iterate over .vc files from system
        for file in config.containers_path.glob("*.vc*"):
            # convert Path to str
            file = str(file)
            # convert filename to vault for dictionary keys
            vault = Vault('').from_container(Path(file))

            # the veracrypt container is mounted
            if file in output:
                print("here")
                # extract the associated line
                for line in output_lines:
                    if file in line:
                        mount_line = line
                        break
                
                info = mount_line.split(' ')
                file, mapper, path = info[1], info[2], info[3]
        
                containers[vault.name] = {'mount': path, 'mapper': mapper}
            else:
                if mounted_only:
                    continue
                else:
                    containers[vault.name] = None
            
        return containers
        
    def list(self):

        containers = self._refresh_list()
        containers = dict(sorted(containers.items()))

        log.info('Available vaults:')
        i = 1
        for key, value in containers.items():
            # unmounted container
            if value is None:
                print(f'{str(i).rjust(2)}: {key.ljust(30)}')
            else:
                mount = value['mount']
                print(f'{str(i).rjust(2)}: {key.ljust(30)} @ {mount} ')

            i = i + 1

    def prune(self):
        # Get the current date
        current_date = datetime.datetime.now()
        no_delete = True

        # Iterate over files in the directory
        for container in config.containers_path.iterdir():
            # Check if it's a file
            if container.is_file():
                # Get the file's creation time
                creation_time = datetime.datetime.fromtimestamp(container.stat().st_ctime)
                # Calculate the difference in days
                difference = (current_date - creation_time).days
                # Check if the file is older than one year
                if difference > 365:
                    # Ask for confirmation
                    # confirmation = input(f"Do you want to delete {file_path.name}? (Yes/No) ").lower()
                    # if confirmation == 'yes':
                    #     # Delete the file
                    #     file_path.unlink()
                    #     print(f"{file_path.name} successfully deleted.")
                    v = Vault('').from_container(container)
                    log.warning(f'{v.name} is older than a year')
                    no_delete = False
        
        if no_delete:
            log.info(f'No containers ready for deletion')
    
