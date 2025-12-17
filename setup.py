from setuptools import setup, Extension
import glob
import os

<<<<<<< HEAD
package_name = "seriapyze"
=======
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
>>>>>>> parent of 4a00248 (pyxact構成変更)

pyi_files = [
    os.path.relpath(f, package_name)
    for f in glob.glob(f"{package_name}/**/*.pyi", recursive=True)
]
package_data = {package_name: pyi_files}

setup(
<<<<<<< HEAD
    name=package_name,
    url="https://github.com/cet-t/seriapyze",
    version="0.1.1",
    description="JSON, YAML, TOML serialization/deserialization for dataclasses",
    author="cet",
    packages=[package_name],
=======
    name="pyxact",
    url="https://github.com/cet-t/pyxact",
    version="0.1.4",
    description="C#-inspired utilities for Python",
    author="cet",
    packages=["pyxact"],
    ext_modules=extensions,
>>>>>>> parent of 4a00248 (pyxact構成変更)
    package_data=package_data,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
