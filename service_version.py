import pathlib

import toml

# Upload toml file
pyproject_path = pathlib.Path("pyproject.toml")
version = toml.load(pyproject_path.open())