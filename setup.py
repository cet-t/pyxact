from setuptools import setup, Extension
import glob
import os

package_name = "seriapyze"

pyi_files = [
    os.path.relpath(f, package_name)
    for f in glob.glob(f"{package_name}/**/*.pyi", recursive=True)
]
package_data = {package_name: pyi_files}

setup(
    name=package_name,
    url="https://github.com/cet-t/seriapyze",
    version="0.1.1",
    description="JSON, YAML, TOML serialization/deserialization for dataclasses",
    author="cet",
    packages=[package_name],
    package_data=package_data,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
