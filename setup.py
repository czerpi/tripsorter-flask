import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="app",
    version="1.0.0",
    description="TripSorter Flask REST API.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage", "requests"]},
)
