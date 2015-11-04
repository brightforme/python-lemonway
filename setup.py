from distutils.core import setup

setup(
    name='python_lemonway',
    version='0.6',
    author='Pierre Pigeau',
    author_email='ppigeau@payplug.com',
    packages=['lemonway'],
    url='',
    license='LICENSE.txt',
    description='',
    long_description=open('README.rst').read(),
    package_data={'lemonway': ['lemonway.wsdl']},
    install_requires=[
        "suds-jurko==0.6",
        "lxml==3.3.5"
    ],
)
