import os

from setuptools import setup

setup(packages=[os.path.join(root).replace("\\", ".") for root, _, files in os.walk("quack") if "__init__.py" in files])
