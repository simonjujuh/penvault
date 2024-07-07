import os
from pathlib import Path

if os.getenv('PENVAULT_ENV') == 'test':
    PENVAULT_PATH   = "/opt/host/penvault/tests/config"
    CONFIG_PATH     = PENVAULT_PATH / "config_test.ini"
    DATA_PATH       = Path(__file__).resolve().parent / "data"
else:
    PENVAULT_PATH   = Path.home() / ".penvault"
    CONFIG_PATH     = PENVAULT_PATH / "config.ini"
    DATA_PATH       = Path(__file__).resolve().parent / "data"