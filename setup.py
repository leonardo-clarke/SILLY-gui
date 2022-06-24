from setuptools import setup, find_packages
import numpy

setup(
    name='silly',
    version='1.0.0',
    include_package_data = True,
    include_dirs=[numpy.get_include()],
    packages=find_packages()
)