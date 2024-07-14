import sys
import configparser
from pathlib import Path
from penvault.logger import log
from penvault.paths import CONFIG_PATH
from penvault.first_run import first_run_setup

first_run_setup()

# Read configuration file
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# THESE OPTIONS HAVE TO EXIST IN THE DEFAULT CONFIG FILE
containers_path = Path(config.get("containers", "containers_path"))
if not containers_path.exists():
    log.error(f"Error while loading config: {containers_path} does not exist")
    sys.exit(1)

mount_path = Path(config.get("containers", "mount_path"))
if not mount_path.exists():
    log.error(f"Error while loading config: {mount_path} does not exist")
    sys.exit(1)


# THESE OPTIONS ARE OPTIONAL IN THE DEFAULT CONFIG FILE
# Vérifiez si la section optionnelle existe
if 'template' in config:
    
    # Accédez aux valeurs de la section optionnelle
    if config.get("template", "template_path"):
        template_path = Path(config.get("template", "template_path"))
        if not template_path.exists():
            log.error(f"Error while loading config: {template_path} does not exist or is empty")
            sys.exit(1)
    else:
        template_path = None
else:
    template_path = None
