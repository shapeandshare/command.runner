import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sacr",
    version="0.3.1",
    author="Joshua C. Burt",
    author_email="joshburt@shapeandshare.com",
    description="Aliased Command Runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["pydantic>=1.9.0"],
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point
    entry_points={
        "console_scripts": ["sacr=shapeandshare.command.runner.command_line:main", "cr=shapeandshare.command.runner.command_line:main"],
    },
)
