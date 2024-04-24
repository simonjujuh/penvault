import sys
import argparse
from penvault.config import mount_path


try:
    import argcomplete
    completion = True
except ImportError:
    completion = False


def build_cli_args():
    parser = argparse.ArgumentParser(description='Pentest Vaults Manager')

    # List
    parser.add_argument('-l', '--list', action='store_true', help='List vaults')
    # Create
    parser.add_argument('-c', '--create', help='Specify the name for the new vault')
    parser.add_argument('-s', '--size', help='Specify the size for the new vault container')
    parser.add_argument('-a', '--auto-mount', action='store_true', default=False, help='Automatically open the newly created container')

    # if completion:
    #     parser.add_argument('-o', '--open', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to open').completer = app.complete_all_vaults
    #     parser.add_argument('-x', '--close', metavar='VAULT', type=str, nargs='+', help='Specify the name of the vault to close').completer = app.complete_opened_vaults
    # else:

    # Open and close
    parser.add_argument('-o', '--open', metavar='VAULT', type=str, nargs='+', help='Open vault(s)')
    parser.add_argument('-x', '--close', metavar='VAULT', type=str, nargs='+', help='Close vault(s)')

    # Resize vaults
    parser.add_argument('-r', '--resize', metavar='VAULT', type=str, nargs='+', help='Resize vault(s) to optimum space')

    # Check options
    parser.add_argument('--check-prune', action='store_true', default=False, help='Delete vaults older than a year')
    parser.add_argument('--no-check-cleanup', action='store_true', default=False, help=f'Do not check for residual directories in {mount_path}')

    # if completion: 
    #     argcomplete.autocomplete(parser)
    
    args = parser.parse_args()


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args

