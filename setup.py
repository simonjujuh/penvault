from setuptools import setup, find_packages

setup(
    name='penvault',
    version='1.1',
    packages=find_packages(),
    package_data={'penvault': ['data/*']},
    entry_points={
        'console_scripts': [
            'penvault=penvault.cli:main',
        ],
    },
)