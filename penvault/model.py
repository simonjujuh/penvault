import sys
import shutil
import subprocess
import string, secrets
from pathlib import Path
from penvault import veracrypt
from penvault import config
from penvault.logger import log

class Vault(object):
    
    def __init__(self, name):
        self.name = name
    
    def to_container(self):
        return config.containers_path / Path(self.name).with_suffix('.vc')

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
            log.success(f"{vc_path.name} mounted: {vault_mount_directory}")
        except Exception as e:
            log.error(f"unable to mount {self.name}: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            vault_mount_directory.rmdir()













class VeracryptContainer(object):

    # def __init__(self, name):
    #     self.path = 
    
    # def to_vault(self):
    #     return self.path.name.with_suffix('').as_posix()





    def open(self):
        pass
    
    def close(self):
        pass
    
    def is_mounted(self):
        pass


class ContainersManager(object):

    def __init__(self):
        pass

    def list(self, only_mounted=False):
        containers = {}

        for file in config.containers_path.glob("*.vc*"):
            containers.update(
                {file: None}
            )
 
        # Command output sample is:
        # 1: /path/to/container.vc  /dev/mapper/veracrypt1  /path/to/mounted/container
        # 2: /path/to/container2.vc  /dev/mapper/veracrypt2  /path/to/mounted/container2
        veracrypt_ouput = veracrypt.list_mounted_containers()
        # If there is at least one mounted container
        if veracrypt_ouput:
            # Iterate over each line
            for line in command_output.stdout.split('\n'):
                if line.strip():
                    info = line.split(' ')
                    file, mapper, path = info[1], info[2], info[3]
                    containers[file] = {'mounted': path, 'mapper': mapper}

        # Display the list of containers
        log.info("Available containers:")

        # Sort the containers dict
        containers = dict(sorted(containers.items()))
        for container, mount_info in containers.items():
            log.success(str(container))
            log.warning(str(mount_info))

    
    def prune(self):
        pass

