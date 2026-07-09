# NRAI path planning

Newcastle Racing AI module for path planning.

To start working on this project, clone this repository.

```bash
git clone --recurse-submodules https://github.com/NewcastleRacingAI/nrai_pathplanning.git
cd nrai_pathplanning
```

## Project structure

```bash
nrai_pathplanning
├── src
│   └── nrai_pathplanning
│       ├── node.py     # Node
│       ├── ...         # Main code
│       └── __init__.py
├── test                # Tests
└── pyproject.toml      # Python package configuration
```

## Use

### Requirements

- [Python>=3.12](https://www.python.org/downloads/release/python-3120/)
- [uv](https://docs.astral.sh/uv/)
  - Can be installed with pip globally

### Setup

Recommended, although not mandatory: create a virtual environment.

```bash
python3 -m venv .venv
# Linux
source .venv/bin/activate
# Windows
.venv/Script/activate
```

We use [uv](https://docs.astral.sh/uv/) to manage the dependencies.
Therefore, you need to install uv, either globally or in the virtual environment:

```bash
pip install uv
```

### Use

Run the script with the following command:

```bash
uv run nrai_pathplanning
```

### Managing dependencies

If you want to add new python dependencies, use `uv add <package>` to add them automatically.

```bash
uv add numpy
```

On the other hand, if you want to remove a dependency, use `uv remove <package>`.

```bash
uv remove numpy
```
