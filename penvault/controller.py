import sys
import os
import yaml
import string, secrets
import shutil
import pykeepass
import getpass
from pathlib import Path
from penvault import veracrypt


class VaultController(object):

    def __init__(self) -> None:
        self._config_dir        = Path.home() / ".penvault"
        self._config_file_path  = self._config_dir / "config.yml" 
        self._data_path         = Path(__file__).resolve().parent / "data"

        self._veracrypt_container_path    = None
        self._veracrypt_mount_path        = None
        self._keepass_database_path       = None
        self._keepass_keyfile_path        = None
        self._keepass_entry_group         = None
        
        self._check_first_run()
        # This will update the None-valued variables above
        self._load_config()

    def _check_first_run(self):
        """
        """
        if not self._config_file_path.exists():
            print("[*] First run detected, installing the configuration file")

            if not self._config_dir.exists():
                self._config_dir.mkdir()

            template_file = self._data_path / "config_template.yml"
            shutil.copyfile(template_file, self._config_file_path)
            print(f"[*] Please edit {self._config_file_path} with the value of your choice...")
            sys.exit(0)

    def _load_config(self):
        """
        """
        with open(self._config_file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        self._veracrypt_container_path  = Path(config['veracrypt']['container_path'])
        self._veracrypt_mount_path      = Path(config['veracrypt']['mount_path'])
        self._keepass_database_path     = Path(config['keepass']['database_path'])
        self._keepass_entry_group       = config['keepass']['entry_title']

        if self._keepass_keyfile_path:
            self._keepass_keyfile_path = Path(config['keepass']['keyfile_path']) 
        else:
            self._keepass_keyfile_path = None

    def _vault_to_container(self, vault_name):
        """
        """
        return self._veracrypt_container_path / Path(vault_name).with_suffix('.vc')

    def _container_to_vault(self, container_name):
        """
        """
        return str(Path(container_name).name)[:-3]
    
    def _prompt_keepass_pwd(self):
        """
        """
        # try:
        password = getpass.getpass(prompt="[*] Please enter your keepass password: ")
        return password

    def _open_keepass_db(self):
        # 0. Prompt for password
        password = self._prompt_keepass_pwd()

        # 1. Check if the keepass db is a real file
        if self._keepass_database_path.is_file():
            # 2. If the keyfile is configured, ensure it is a real file
            if self._keepass_keyfile_path and not self._keepass_keyfile_path.is_file():
                print(f"[-] keyfile '{self._keepass_keyfile_path}' not found")
                raise Exception

            # 3. Open the keepass database
            kpcon = pykeepass.PyKeePass(self._keepass_database_path, password=password, keyfile=self._keepass_keyfile_path)
            if not kpcon:
                raise Exception
            else:
                print(f"[+] keepass database '{self._keepass_database_path}' opened successfully")
                return kpcon
        else:
            print(f"[-] keepass database '{self._keepass_database_path}' not found")
            raise Exception

    def create_vault(self, vault_name, vault_size, auto_mount=False):
        # Get the vault name
        container_path = Path(self._vault_to_container(vault_name))

        # Generate random password
        length = 30
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Do not overwrite an existing container
        if container_path.exists():
            print(f"[-] container '{container_path}' already exists, please use another vault name")
            sys.exit(1)

        # Create a container
        veracrypt.create_container(container_path, vault_size, password)

        try:
            # Connect to the database
            keepass_con = self._open_keepass_db()

            # Find the group to store the entry
            # NOTE the case where multiple groups are found will not occurs due to parameter first=true
            group_found = keepass_con.find_groups(name=self._keepass_entry_group, first=True)
            # Case where the group does not exists; then create it
            if not group_found:
                keepass_con.add_group(keepass_con.root_group, self._keepass_entry_group)
                keepass_con.save()
                print(f"[+] group '{self._keepass_entry_group}' created in keepass database")
                group_found = keepass_con.find_groups(name=self._keepass_entry_group, first=True)
            
            # Search the entry in keepass
            entry = keepass_con.find_entries(title=vault_name, first=True)

            if entry:
                print(f"[*] entry for vault '{vault_name}' already exists")
                print("[*] saving the current entry password in history")
                # Add current password to history
                entry.save_history()
                entry.password = password
            else:
                keepass_con.add_entry(group_found, vault_name, str(container_path), password)
            
            # Save changes to the database
            print("[*] keepass database updated")
            keepass_con.save()

        except Exception as e:
            print(f"[-] failure to perform keepass action: {e}")
            print(f"    removing container '{container_path}'")
            os.remove(str(container_path))
        finally:
            if auto_mount:
                veracrypt.mount_container(container_path, self._veracrypt_mount_path, password)

    def open_vault(self, vault_name):
        # Get the vault name
        container_path = Path(self._vault_to_container(vault_name))

        # Check if container path exists
        if not container_path.exists():
            print(f"[-] container '{container_path}' does not exist, exiting.")
            sys.exit(1)

        # Check if veracrypt mount path exists
        if not self._veracrypt_mount_path.exists():
            print(f"[-] mount point path '{self._veracrypt_mount_path}' does not exist, abort.")
            sys.exit(1)
        
        # Open keepass database
        try:
            # Connect to the database
            keepass_con = self._open_keepass_db()

            # Find the group to store the entry
            # NOTE the case where multiple groups are found will not occurs due to parameter first=true
            group_found = keepass_con.find_groups(name=self._keepass_entry_group, first=True)
            # Case where the group does not exists; then create it
            if not group_found:
                keepass_con.add_group(keepass_con.root_group, self._keepass_entry_group)
                keepass_con.save()
                print(f"[+] group '{self._keepass_entry_group}' created in keepass database")
                group_found = keepass_con.find_groups(name=self._keepass_entry_group, first=True)
            
            # Search the entry in keepass
            entry = keepass_con.find_entries(title=vault_name, first=True)

            if entry:
                print(f"[*] entry found for vault '{vault_name}'")
                container_password = entry.password
            else:
                raise Exception

        except Exception as e:
            print(f"[-] failed to open '{container_path}', removing it")
            print(f"[-] exception: {e}")

        # Mount container
        directory_path = self._veracrypt_mount_path / vault_name

        # Creating the directory if it doesn't exist
        directory_path.mkdir(parents=False, exist_ok=True)
        veracrypt.mount_container(container_path, directory_path, container_password)

    def list_vaults(self):
        """
        """
        # Fetch the mounted container list
        mounted_containers = veracrypt.list_mounted_containers()

        # Get .vc containers from the filesystem
        # Use a regular expression to filter VeraCrypt files
        veracrypt_fs_containers = list([str(e) for e in self._veracrypt_container_path.glob("*.vc*")])
        print("[*] available containers:")
        for container in mounted_containers:
            vault = self._container_to_vault(container['path'])
            print(f"  - {vault} (mounted at '{container['mount point']}')")
            veracrypt_fs_containers.remove(container['path'])

        for container in veracrypt_fs_containers:
            vault = self._container_to_vault(container)
            print(f"  - {vault}")


    def close_vault(self, vault_name):
        container_name = self._vault_to_container(vault_name)

        # Check if container is mounted or not
        mounted_containers = [entry['path'] for entry in veracrypt.list_mounted_containers()]
        if not str(container_name) in mounted_containers:
            print(f"[-] container '{container_name}' not mounted")
            sys.exit(1)
        
        veracrypt.umount_container(container_name)
        directory_path = self._veracrypt_mount_path / vault_name
        if directory_path.exists():
            directory_path.rmdir()

    def complete_vaults(self, prefix, parsed_args, **kwargs):
        veracrypt_fs_containers = []

        for e in self._veracrypt_container_path.glob("*.vc*"):
            v = self._container_to_vault(e)
            veracrypt_fs_containers.append(v)

        return (vault for vault in veracrypt_fs_containers if vault.startswith(prefix))