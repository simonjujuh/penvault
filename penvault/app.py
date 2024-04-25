import sys
from penvault.config import containers_path, mount_path
from penvault.cli import build_cli_args
from penvault.logger import log
from penvault.model import VaultsManager, Vault

def main():
    args = build_cli_args()
    
    # Create instances
    manager = VaultsManager()


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
        for vault_name in args.open:
            Vault(vault_name).open()

    # penvault.py --resize <VAULT>
    elif args.resize:
        # resize accept mutliple vaults
        for vault in args.resize:
            pass

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
    elif args.check_prune:
        manager.prune()

if __name__ == '__main__':
    main()
    sys.exit(0)
