import sys
import getpass
from penvault.config import containers_path, mount_path, template_path
from penvault.cli import build_cli_args
from penvault.logger import log
from penvault.model import VaultsManager, Vault

def main():
    args = build_cli_args()
    
    # Create instances
    manager = VaultsManager()

    if args.check_cleanup:
        manager.cleanup()

    if args.create:
        if not args.size:
            log.error("The --size option is required when --create is selected")
            sys.exit(1)
        else:
            vault = Vault(args.create)
            vault.create(args.size, auto_mount=args.auto_mount, template_path=template_path)
    
    # penvault.py --open <VAULT>
    elif args.open:
        # open accept mutliple vaults
        for vault_name in args.open:
            Vault(vault_name).open()

    # penvault.py --archive <VAULT>
    elif args.archive:
        # resize accept mutliple vaults
        for vault_name in args.archive:
            try:
                # Prompting the user for a password
                password = getpass.getpass(f'Enter {vault_name} password: ')
            except Exception as error:
                print('Error while prompting password:', error)
            
            vault = Vault(vault_name).archive(password=password)

    # penvault.py --close <VAULT>
    elif args.close:
        # close accept mutliple vaults
        for vault_name in args.close:
            Vault(vault_name).close()

    # Available containers:
    # 01: vault 1 </path/>
    # 02: vault 2
    # 03: vault 3
    # 04: vault 4 </path/>
    elif args.list: 
        manager.list()

    if args.check_prune:
        manager.prune()
    

if __name__ == '__main__':
    main()
    sys.exit(0)
