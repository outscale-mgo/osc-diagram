
[![Project Sandbox](https://docs.outscale.com/fr/userguide/_images/Project-Sandbox-yellow.svg)](https://docs.outscale.com/en/userguide/Open-Source-Projects.html)

# Outscale Diagram

This project serve as examples for diagram, and as a lib to show diagrams of your cloud.

## usage
just call
```
 osc-diagram
 ```
 
it will create an image `all-vms.png` and an `all-vms.dot`

## Installing from sources

It is a good practice to create a [dedicated virtualenv](https://virtualenv.pypa.io/en/latest/) first. Even if it usually won't harm to install Python libraries directly on the system, better to contain \
dependencies in a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

macos require graphviz:
```zsh
brew install graphviz
```
