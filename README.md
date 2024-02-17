# Audit vaults

## Installation

- Install the dependencies
```bash
sudo apt install veracrypt keepassxc
```

- Basic usage
```bash
python3 penvault.py list
python3 penvault.py create <vault_name> --auto-mount
python3 penvault.py mount <vault_name>
python3 penvault.py umount <vault_name>
```

## To-Do

- [ ] Make zsh completion scripts
- [ ] Make bash completion scripts
- [ ] Implement the prune feature
- [ ] Color highlights

## Aliases

```bash
alias pvl=''
alias pvc=''
alias pvo=''
alias pvcl=''
```