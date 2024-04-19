#!/usr/bin/env python3

import sys
import argparse
from penvault.controller import VaultController

try:
    import argcomplete
    completion = True
except ImportError:
    completion = False


def main():
    app = VaultController()

    # Parse command line
    parser = argparse.ArgumentParser(description='Pentest Vaults Manager')
    parser.add_argument('-l', '--list', action='store_true', help='List vaults')
    parser.add_argument('-c', '--create', help='Specify the name for the new vault')
    parser.add_argument('-s', '--size', help='Specify the size for the new vault container')
    parser.add_argument('-a', '--auto-mount', action='store_true', default=False, help='Automatically open the newly created container')

    if completion:
        parser.add_argument('-o', '--open', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to open').completer = app.complete_all_vaults
        parser.add_argument('-x', '--close', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to close').completer = app.complete_opened_vaults
    else:
        parser.add_argument('-o', '--open', help='Specify the name of the vault to open')
        parser.add_argument('-x', '--close', help='Specify the name of the vault to close')

    parser.add_argument('--show-config', action='store_true', default=False, help='Automatically open the newly created container')

    if completion: 
        argcomplete.autocomplete(parser)
    
    args = parser.parse_args()

    if args.create:
        if not args.size:
            parser.error("The --size option is required when --create is selected")
        else:
            app.create_vault(args.create, args.size, args.auto_mount)
    elif args.open:
        for vault in args.open:
            app.open_vault(vault)
    elif args.close:
        for vault in args.close:
            app.close_vault(vault)
    elif args.list:
        app.list_vaults()
    elif args.show_config:
        app.show_app_config()
    else:
        parser.print_help() 
    # elif args.mode == 'prune':
    #     prune_projects(args.option_prune)

if __name__ == '__main__':
    main()
    sys.exit(0)