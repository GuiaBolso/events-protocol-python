from os.path import dirname, join
from setuptools import setup, find_packages


with open(join(dirname(__file__), "events_protocol/VERSION")) as _file:
    version = _file.read().strip()


with open(join(dirname(__file__), "README.md")) as _file:
    long_description = _file.read()


setup(
    name="events-protocol",
    version=version,
    author="Guiabolso",
    description="Library to be a Client and Server using event protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuiaBolso/events-protocol-python",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=[
        "certifi==2019.11.28",
        "chardet==3.0.4",
        "dataclasses-json==0.3.7",
        "idna==2.8",
        "marshmallow==3.3.0",
        "marshmallow-enum==1.5.1",
        "mypy-extensions==0.4.3",
        "requests==2.22.0",
        "stringcase==1.2.0",
        "typing-extensions==3.7.4.1",
        "typing-inspect==0.5.0",
        "urllib3==1.25.8",
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
