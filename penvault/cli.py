import sys
import argparse
from penvault.completion import *
from penvault.config import mount_path

VERSION = "1.2.0-dev" # to change

def build_cli_args():

    try:
        import argcomplete
        completion = True
    except ImportError:
        completion = False

    parser = argparse.ArgumentParser(description=f'Pentest Vaults Manager {VERSION}')

    # List options
    parser.add_argument('-l', '--list', action='store_true', help='List vaults')
    
    # Create options
    parser.add_argument('-c', '--create', help='Specify the name for the new vault')
    parser.add_argument('-s', '--size', help='Specify the size for the new vault container')
    parser.add_argument('-a', '--auto-mount', action='store_true', default=False, help='Automatically open the newly created container')

    # Open, close and archive options
    if completion:
        parser.add_argument('-o', '--open', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to open', choices=complete_all_vaults())
        parser.add_argument('-x', '--close', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to close', choices=complete_opened_vaults())
        parser.add_argument('-z', '--archive', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to archive', choices=complete_all_vaults())

    else:
        parser.add_argument('-o', '--open', metavar='VAULT', type=str, nargs='+', help='Open vault(s)')
        parser.add_argument('-x', '--close', metavar='VAULT', type=str, nargs='+', help='Close vault(s)')
        parser.add_argument('-z', '--archive', metavar='VAULT', type=str, nargs='+', help='Archive vault(s)')

    # Check options
    parser.add_argument('--check-prune', action='store_true', default=False, help='Delete vaults older than a year')
    parser.add_argument('--check-cleanup', action='store_true', default=True, help=f'Check for residual directories in {mount_path} (default: True)')

    if completion: 
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args

