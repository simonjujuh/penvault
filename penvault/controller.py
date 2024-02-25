import sys
import yaml
import string, secrets
import shutil
from pathlib import Path
from penvault import veracrypt
from penvault.logger import log


class VaultController(object):

    def __init__(self) -> None:
        self._config_dir        = Path.home() / ".penvault"
        self._config_file_path  = self._config_dir / "config.yml" 
        self._data_path         = Path(__file__).resolve().parent / "data"

        self._veracrypt_container_path    = None
        self._veracrypt_mount_path        = None

        self._check_first_run()
        # This will update the None-valued variables above
        self._load_config()

    def _check_first_run(self):
        """
        """
        if not self._config_file_path.exists():
            log.info("first run detected, installing the configuration file")

            if not self._config_dir.exists():
                self._config_dir.mkdir()

            template_file = self._data_path / "config_template.yml"
            shutil.copyfile(template_file, self._config_file_path)
            log.info(f"please edit {self._config_file_path} with the value of your choice...")
            sys.exit(0)

    def _load_config(self):
        """
        """
        with open(self._config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        self._veracrypt_container_path  = Path(config['veracrypt']['container_path'])
        self._veracrypt_mount_path      = Path(config['veracrypt']['mount_path'])

    def show_app_config(self):
        log.success(f"Config file is {self._config_file_path}")
        log.info(f"Veracrypt containers: {self._veracrypt_container_path}")
        log.info(f"Veracrypt mount path: {self._veracrypt_mount_path}")

    def _vault_to_container(self, vault_name):
        """
        """
        return self._veracrypt_container_path / Path(vault_name).with_suffix('.vc')

    def _container_to_vault(self, container_name):
        """
        """
        return str(Path(container_name).name)[:-3]

    def create_vault(self, vault_name, vault_size, auto_mount=False):
        # Get the vault name
        container_path = Path(self._vault_to_container(vault_name))

        # Generate random password
        length = 30
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Do not overwrite an existing container
        if container_path.exists():
            log.error(f"container '{container_path}' already exists, please use another vault name")
            sys.exit(1)

        # Create a container
        try:
            veracrypt.create_container(container_path, vault_size, password)
            log.success(f"container '{container_path}' created successfully")
            log.info(f"password: {password}")
        except Exception as e:
            log.error(f"unable to create '{container_path}': {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            pass
        finally:
            if auto_mount:
                veracrypt.mount_container(container_path, self._veracrypt_mount_path, password)

    def open_vault(self, vault_name):
        # Get the vault name
        container_path = Path(self._vault_to_container(vault_name))

        # Check if container path exists
        if not container_path.exists():
            log.error(f"container '{container_path}' does not exist, exiting.")
            sys.exit(1)

        # Check if veracrypt mount path exists
        if not self._veracrypt_mount_path.exists():
            log.error(f"mount point path '{self._veracrypt_mount_path}' does not exist, abort.")
            sys.exit(1)
        
        # Mount container
        directory_path = self._veracrypt_mount_path / vault_name

        # Creating the directory if it doesn't exist
        try:
            directory_path.mkdir(parents=False, exist_ok=True)
            veracrypt.mount_container(container_path, directory_path, '') # empty password means it will be prompted
            log.success(f"container '{container_path}' mounted successfully")
        except Exception as e:
            log.error(f"unable to mount '{container_path}': {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            directory_path.rmdir()

    def list_vaults(self):
        """
        """
        # Fetch the mounted container list
        mounted_containers = veracrypt.list_mounted_containers()

        # Get .vc containers from the filesystem
        # Use a regular expression to filter VeraCrypt files
        veracrypt_fs_containers = [str(e) for e in self._veracrypt_container_path.glob("*.vc*")]
        veracrypt_fs_containers.sort()

        log.info("available containers:")
        for container in mounted_containers:
            vault = self._container_to_vault(container['path'])
            print(f"  - {vault.ljust(40)} (mounted at '{container['mount point']}')")
            veracrypt_fs_containers.remove(container['path'])

        for container in veracrypt_fs_containers:
            vault = self._container_to_vault(container)
            print(f"  - {vault}")

    def close_vault(self, vault_name):
        container_path = self._vault_to_container(vault_name)

        # Check if container is mounted or not
        mounted_containers = [entry['path'] for entry in veracrypt.list_mounted_containers()]
        if not str(container_path) in mounted_containers:
            log.error(f"container '{container_path}' not mounted")
            sys.exit(1)
        
        try:
            veracrypt.umount_container(container_path)
            log.success(f"container '{container_path}' unmounted successfully")
        except Exception as e:
            log.error(f"unable to unmount '{container_path}': {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            pass
        else:
            directory_path = self._veracrypt_mount_path / vault_name
            if directory_path.exists():
                directory_path.rmdir()

    def complete_vaults(self, prefix, parsed_args, **kwargs):
        veracrypt_fs_containers = []

        for e in self._veracrypt_container_path.glob("*.vc*"):
            v = self._container_to_vault(e)
            veracrypt_fs_containers.append(v)

        return (vault for vault in veracrypt_fs_containers if vault.startswith(prefix))