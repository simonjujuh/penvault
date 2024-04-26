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
containers_path = Path(config.get("containers", "veracrypts_path"))
if not containers_path.exists():
    log.error(f"error while loading config: {containers_path} does not exist")
    sys.exit(1)

mount_path = Path(config.get("containers", "mount_path"))
if not mount_path.exists():
    log.error(f"error while loading config: {mount_path} does not exist")
    sys.exit(1)