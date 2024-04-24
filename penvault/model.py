import shutil
import subprocess
from pathlib import Path

class Vault(object):
    
    def __init__(self, name):
        self.name = name
    
    def to_container(self):
        pass


class VeracryptContainer(object):

    def __init__(self, name):
        self.path = Path(path)
    
    def to_vault(self):
        pass

    def create(self):
        pass

    def open(self):
        pass
    
    def close(self):
        pass


class ContainersManager(object):

    def __init__(self):
        pass

    def list(self, only_mounted=False):
        pass
    
    def prune(self):
        pass