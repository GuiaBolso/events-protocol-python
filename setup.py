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
        "certifi>=2019.11.28",
        "chardet>=3.0.4",
        "idna>=2.8",
        "pydantic>=1.4",
        "requests>=2.22.0",
        "urllib3>=1.25.8",
    ],
    extras_require={"doc": ["Sphinx==2.4.1", "sphinx-autoapi==1.2.1",],},
    project_urls={
        "Documentation": "https://events-protocol.readthedocs.io/en/stable/",
        "Source Code": "https://github.com/GuiaBolso/events-protocol-python",
    },
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
