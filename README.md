# PenVaults

**WARNING**: this is an early work, please use it with caution and report any bug.

## Description
Manage and automate pentest vaults creation with associated keepass entries.

## Installation

- Install the dependencies
```bash
sudo apt install veracrypt
pip install .
```
- Basic usage
```bash
penvault --list
penvault --create VAULT_NAME --size 10G
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
- [x] Color highlights
- [ ] Add pentest template folder
- [ ] Add pentest cheat sheets / MVP
- [ ] Use a dedicated keepass db for containers
- [ ] Implement the prune feature
- [ ] Make dedicated completion function for open and close
- [x] Review log messages consistence
- [x] Fix auto-open path