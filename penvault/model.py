import sys, os
import string, secrets
import datetime
import shutil
import tempfile
from colorama import init, Fore, Style
from pathlib import Path
from penvault import veracrypt
from penvault import config
from penvault.logger import log


class Vault(object):
    """
    A class to manage pentest vaults securely with GPG or Veracrypt.

    Vaults are abstract projects name, described with a single name. Containers, on 
    the other hand refer to the associated full path on the system, ending with
    .gpg or .vc extension.
    """
    
    def __init__(self, name):
        self.name = name
        
        # Check objects attributes values
        if self.name.endswith('.vc'):
            raise ValueError("Vault object cannot end with '.vc' extension")

    def _to_file_path(self):
        return config.containers_path / Path(self.name).with_suffix('.vc')

    def _from_file_path(self, container_path):
        return Vault(container_path.with_suffix('').name)

    def create(self, size, auto_mount=False, template_path=None):
        # Get the vault name
        container_path = self._to_file_path()

        # Generate random password
        length = 30
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Do not overwrite an existing container
        if container_path.exists():
            log.error(f"{container_path} already exists, please use another vault name")
            sys.exit(1)
        else:
            # Create a Veracrypt container
            try:
                veracrypt.create_container(container_path, size, password)
                log.success(f"{self.name} created successfully with password {password}")
            except Exception as e:
                log.error(f"unable to create {container_path}: {e}")
                sys.exit(1)
        
        # Open the freshly created container
        self.open(password)

        # If template folder is configured, copy it
        if template_path:
            log.info(f"Template {template_path} is configured and will be copied")
            # Copy template path
            mounted_at = config.mount_path / self.name

            # Ensure that the directory is mounted
            if mounted_at:
                # Copy the template to the mounted directory
                for item in template_path.iterdir():
                    if item.is_dir():
                        shutil.copytree(item, mounted_at / item.name)
                    else:
                        shutil.copy2(item, mounted_at)
            else:
                log.warning(f"Could not copy template because {mounted_at} does not exist")

        # If auto mount is not selected, close the created container
        if not auto_mount:
            self.close()
           
    def open(self, password=''):
        # Get the vault name
        container_path = self._to_file_path()

        # Check if container path exists
        if not container_path.exists():
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
            veracrypt.mount_container(container_path, vault_mount_directory, password) # empty password means it will be prompted
            log.success(f"{self.name} mounted: {vault_mount_directory}")
        except Exception as e:
            log.error(f"unable to mount {self.name}: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            vault_mount_directory.rmdir()

    def close(self):
        container_path = self._to_file_path()

        # Check if container is mounted or not
        if not self.is_mounted():
            log.error(f"{self.name} not mounted, exiting")
            sys.exit(1)

        try:
            veracrypt.umount_container(container_path)
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

    def archive(self, password=''):
        """
        Convert a Veracrypt container to an tar.gz encrypted archive, mainly for storage purpose
        """
        log.info("Starting to archive {self.name}")

        # Open the vault
        self.open(password)

        # Change owner of all stored files

        # # Get the current user's UID and GID
        # if user is None:
        #     user = os.getenv("USER")
            
        # uid = int(subprocess.check_output(['id', '-u', user]))
        # gid = int(subprocess.check_output(['id', '-g', user]))

        # # Change ownership for all files and directories in the given path
        # for root, dirs, files in os.walk(path):
        #     for momo in dirs + files:
        #         momo_path = Path(root) / momo
        #         log.info(f"Changing ownership of {momo_path} to {user} (UID: {uid}, GID: {gid})")
        #         os.chown(momo_path, uid, gid)

        # Make a temporary directory
        with tempfile.TemporaryDirectory(dir=config.containers_path) as temp_dir:
            temp_path = Path(temp_dir)

            # Move vault content to the temporary directory  
            try:
                src_path = Path(self.mount_point())
                
                # Ensure the directories exists
                if not src_path.exists():
                    raise FileNotFoundError(f"The directory '{src_path}' does not exist")

                shutil.copytree(src_path, temp_path)
                log.info(f"The directory '{src_dir}' was moved to '{dst_dir}'")
            except Exception as e:
                print(f"An error occured while moving veracrypt content: {e}")

        # Rename temporary directory
        archive_directory = str(self.containers_path / self.name.with_suffix(''))
        shutil.move(str(temp_path), archive_directory)

        # 

        # Delete veracrypt vault
        # TODO

    def mount_point(self):
        container_path = self._to_file_path()

        import re
        pattern = re.compile(rf"{str(container_path)}\s+/dev/mapper/veracrypt\d+\s+({str(config.mount_path)}.+)$")
        match = pattern.search(veracrypt.list_mounted_containers())
        if match:
            return match.group(1)
        else:
            return None

    def is_mounted(self):
        if self.mount_point():
            return True
        else:
            return False


class VaultsManager(object):

    def __init__(self):
        pass

    # TODO améliorer cette fonction pour supporter les fonctions mount_point et is_mounted
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
            vault = Vault('')._from_file_path(Path(file))

            # the veracrypt container is mounted
            if file in output:
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
                    v = Vault('')._from_file_path(container)
                    log.warning(f'{v.name} is older than a year')
                    no_delete = False
        
        if no_delete:
            log.info(f'No containers ready for deletion')
    
    def cleanup(self):
        # List directories in the config.mount_path
        directories = [entry for entry in config.mount_path.iterdir() if entry.is_dir()]
        
        # Check each directory
        for directory in directories:
            # Check if the directory is present in the list of mounted containers
            if directory.name in veracrypt.list_mounted_containers():
                # If yes, move to the next directory
                continue
            else:
                empty = True
                for _ in directory.iterdir():
                    # If there's at least one item, the directory is not empty
                    empty = False

                if empty:
                    # If not, print a warning and optionally remove the directory
                    # Remove the directory (use with caution)
                    while True:
                        user_input = input(Fore.YELLOW + "[!] " 
                                           + Style.RESET_ALL 
                                           + f"'{directory}' is a residual folder, do you want to delete it? [y/N] ").strip().lower()
                        if user_input == 'y':
                            directory.rmdir()
                            log.info(f"'{directory}' deleted")
                            break
                        elif user_input == 'n' or user_input == '':
                            log.info(f"'{directory}' not deleted")
                            break
                        else:
                            continue


