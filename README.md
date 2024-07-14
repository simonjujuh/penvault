# Penvaults

Helps you manage your pentest vercarypt containers (vaults) easily.

> **Disclaimer**: This tool is currently under active development, and as such, you may encounter bugs, incomplete features, and other issues. We recommend using it with caution. If you find any bugs or have suggestions, please report them via our GitHub issue tracker. We appreciate community contributions and feedback to help us improve. Note that this project is provided "as is" without any warranties, and we are not responsible for any damage or data loss incurred while using this tool. Thank you for your understanding and support!

## Installation

* First, you need to install veracrypt (cli and gui)

* Install the script

```bash
# Download the builder
pip3 install build

# Clone the repository
git clone https://github.com/simonjujuh/penvault && cd penvault
python3 -m build
pip3 install dist/penvault-$VERSION-py3-none-any.whl
```

* On the first run, penvault will create a configuration file in `~/.penvault/config.ini`. Edit this file with the desired options

```ini
[containers]
container_path = /path/to/containers/folder
mount_path = /path/to/containers/mountpoint

; This one below is optional, you can comment it with ';' in front of each line
[template]
template_path = /path/to/your/template
```

## Autocompletion

To enable the completion feature supported by the script, please use the below commands:

```bash
pip install argcomplete
activate-global-python-argcomplete
# Add this line to your zshrc / bashrc 
eval "$(register-python-argcomplete penvault)"
```

## Coming soon (to-do)

* [x] Add an autoresize or archive feature for vaults
* [ ] Add multiple pentest folders
* [ ] Check and test the prune feature
* [ ] Manage less passwords by using keepass
