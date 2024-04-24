from pathlib import Path

PENVAULT_PATH   = Path.home() / ".penvault"
CONFIG_PATH     = PENVAULT_PATH / "config.ini"
DATA_PATH       = Path(__file__).resolve().parent / "data"