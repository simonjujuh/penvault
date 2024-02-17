from setuptools import setup, find_packages

setup(
    name='penvault',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'penvault=penvault.cli:main',  # Remplacez 'cli' par le nom de votre fichier principal
        ],
    },
)