import sys
import shutil
from penvault.logger import log
from penvault.paths import CONFIG_PATH, PENVAULT_PATH, DATA_PATH


def first_run_setup():
    # $HOME/.penvault/config.ini does not exist 
    if not CONFIG_PATH.exists():
        log.info("first run detected, installing the configuration file")
        
        # $HOME/.penvault/ does not exist, create it
        if not PENVAULT_PATH.exists():
            PENVAULT_PATH.mkdir()

        # Copy template configuration file to ~/.penvault/config.ini
        template_file = DATA_PATH / "config.ini"
        shutil.copyfile(template_file,CONFIG_PATH)

        # Inform end user to change config and exit
        log.info(f"please edit {CONFIG_PATH} with the value of your choice...")
        sys.exit(0)