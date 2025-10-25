from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
import os

pyx_files = glob.glob("pyxact/**/*.pyx", recursive=True)

extensions = cythonize(
    [
        Extension(file.replace("/", ".").replace("\\", ".").replace(".pyx", ""), [file])
        for file in pyx_files
    ],
    compiler_directives={"language_level": "3"},
)

pyi_files = [
    os.path.relpath(f, "pyxact") for f in glob.glob("pyxact/**/*.pyi", recursive=True)
]
package_data = {"pyxact": pyi_files}
from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
import os

pyx_files = glob.glob("pyxact/**/*.pyx", recursive=True)

extensions = cythonize(
    [
        Extension(file.replace("/", ".").replace("\\", ".").replace(".pyx", ""), [file])
        for file in pyx_files
    ],
    compiler_directives={"language_level": "3"},
)

pyi_files = [
    os.path.relpath(f, "pyxact") for f in glob.glob("pyxact/**/*.pyi", recursive=True)
]
package_data = {"pyxact": pyi_files}

setup(
    name="pyxact",
    url="https://github.com/cet-t/pyxact",
    version="0.1.0",
    description="C#-inspired utilities for Python",
    author="cet",
    packages=["pyxact"],
    ext_modules=extensions,
    package_data=package_data,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
