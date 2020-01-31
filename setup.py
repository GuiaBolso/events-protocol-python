from os.path import dirname, join
from setuptools import setup, find_packages

import events_protocol



with open(join(dirname(__file__), "README.md")) as _file:
    long_description = _file.read()


setup(
    name="events-protocol",
    version=events_protocol.__version__,
    author="Guiabolso",
    description="Library to be a Client and Server using event protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuiaBolso/events-protocol-python",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=[
        "pydantic==1.3",
        "requests==2.22.0"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
