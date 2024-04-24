import shutil
import sys
import configparser
from pathlib import Path


class Config(object):
    # Configuration directory and file 
    CONFIG_DIR          = Path.home() / ".penvault"
    CONFIG_FILE_PATH    = CONFIG_DIR / "config.ini"
    DATA_PATH           = Path(__file__).resolve().parent / "data"
    
    def __init__(self):
        self._check_first_run()
    
    def _check_first_run(self):
        # The config file does not exist
        if not self.CONFIG_FILE_PATH.exists():
            log.info("first run detected, installing the configuration file")

            # The config directory doesn't exist either
            if not self.CONFIG_DIR.exists():
                self.CONFIG_DIR.mkdir()

            # Copy the template config file to the config directory
            template_file = self.DATA_PATH / "config.ini"
            shutil.copyfile(template_file, self.CONFIG_FILE_PATH)
            log.info(f"please edit {self.CONFIG_FILE_PATH} with the value of your choice...")
            sys.exit(0)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE_PATH)
        return config


# Load configuration
cfg = Config().load_config()

if __name__ == '__main__':
    pass