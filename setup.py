from os.path import dirname, join
from setuptools import setup, find_packages


with open(join(dirname(__file__), "events_protocol/VERSION")) as _file:
    version = _file.read().strip()


with open(join(dirname(__file__), "README.md")) as _file:
    long_description = _file.read()


setup(
    name="events-protocol",
    version=version,
    description="Library to be a Client and Server using event protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuiaBolso/events-protocol-python",
    license="Apache-2.0",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache-2.0 License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
