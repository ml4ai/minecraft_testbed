# BaseAgent



## Installation

The BaseAgent package can be installed via `pip`.  A basic install can be done from the root folder of the package with the following command:

    pip install --user -e .

To install with all extras:

    pip install --user -e .[all]

## Requirements

This package depends on the following repos:
- [`MinecraftBridge`](https://gitlab.com/cmu_asist/MinecraftBridge) (version >= 1.3.0)
- [`RedisBridge`](https://gitlab.com/cmu_asist/RedisBridge) (version >= 1.1.0)

These can be pip-installed as extras. From the root BaseAgent folder, run:

    pip install --user -e .[<package_name>]

If you prefer to install from source, or you already have a package installed locally and want to avoid overriding it with remote versions, simply omit it from the extras on installation.
