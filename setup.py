from setuptools import find_packages
from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='python-lemonway',
    version='0.7.0',
    author='Pierre Pigeau',
    author_email='ppigeau@payplug.com',
    packages=['lemonway'],
    url='',
    license='LICENSE.txt',
    description='Lemonway API python library',
    long_description=long_description,
    include_package_data = True,
    install_requires=[
        "suds-jurko",
        "lxml",
        "xmltodict"
    ],
)
