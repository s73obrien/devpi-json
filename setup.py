from setuptools import setup
import os

setup(
    name='devpi-json',
    description='devpi-json',
    long_description='',
    entry_points = {
        'devpi_server': [
            'devpi-json = devpi_json.main'
        ]
    },
    include_package_data = True,
    zip_safe = False,
    packages = ['devpi_json']
)

