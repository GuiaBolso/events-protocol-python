from os.path import dirname, join
from setuptools import setup, find_packages


with open(join(dirname(__file__), 'events-protocol-core/VERSION')) as _file:
    version = _file.read().decode('ascii').strip()


setup(
    name='events-protocol-core',
    version=version,
    description='Core library for client and server libs',
    license='Apache-2.0',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache-2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
