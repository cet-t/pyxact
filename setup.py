from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
import os

pyi_files = [
    os.path.relpath(f, "pyxact") for f in glob.glob("pyxact/**/*.pyi", recursive=True)
]
package_data = {"pyxact": pyi_files}

setup(
    name="pyxact",
    url="https://github.com/cet-t/pyxact",
    version="0.1.10",
    description="C#-inspired utilities for Python",
    author="cet",
    packages=["pyxact"],
    package_data=package_data,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
