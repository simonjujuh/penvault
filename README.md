# PenVaults

**WARNING**: this is an early work, please use it with caution and report any bug.

## Description
Manage and automate pentest vaults creation with associated keepass entries.

## Installation
- Install the dependencies
```bash
sudo apt install veracrypt
pip install --user .
```
- Basic usage
```bash
penvault --list
penvault --create VAULT_NAME --size 10G --auto-mount
penvault --open VAULT_NAME
penvault --close VAULT_NAME
penvault --show-config
```

## Bash / ZSH completion
```bash
pip install argcomplete
activate-global-python-argcomplete
# Add this line to your zshrc / bashrc 
eval "$(register-python-argcomplete penvault)"
```

## To-Do
- [ ] Add an autoresize feature
- [ ] Add pentest template folder
- [x] Implement the prune feature
- [x] Execute without argcomplete
- [x] Order completions
- [ ] Use a dedicated keepass DB for containers
