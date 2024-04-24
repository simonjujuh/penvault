
import configparser
from pathlib import Path
from penvault.logger import log
from penvault.paths import CONFIG_PATH

# Read configuration file
default_config = configparser.ConfigParser()
default_config.read(CONFIG_PATH)

# THESE OPTIONS HAVE TO EXIST IN THE DEFAULT CONFIG FILE
containers_path = Path(config.get("containers", "veracrypts_path"))
if not container_path.exists():
    log.error(f"error while loading config: {container_path} does not exists")
    sys.exit(1)

mount_path = Path(config.get("containers", "mount_path"))
if not mount_path.exists():
    log.error(f"error while loading config: {container_path} does not exists")
    sys.exit(1)
