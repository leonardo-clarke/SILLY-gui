from setuptools import setup, find_packages
import numpy

setup(
    name='SILLY-gui',
    version='1.0.2',
    include_package_data = True,
    include_dirs=[numpy.get_include()],
    packages=find_packages()
)