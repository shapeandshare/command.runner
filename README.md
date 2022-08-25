# [S]hape and Share [A]liased [C]ommand [R]unner - SACR

## Overview
SACR is meant to be a simple add-in for Python centric project management.  I wanted tooling similair to what NPM provides within the Node.js ecosystem or make for compiled application.

There are a number of tools out there but none of them worked with multiple commands and integrated well.

## Functionality
* Command execution (and chaining)
  * Support for Python ini files (and running sets of commands from a single alias)
  * Support for NPM package.json files
* Project cleanup support

## Installation
To download and install the latest version simply perform a pip install:
> pip install sacr

## Initial configuration
If you are setting up a new project or want to create the defaults run the following:
> sacr init

This will create two new files within the current project:
1. `.sacrrc` - This file handles application configuration and functionality for the current solution.  Here you configure command time outs and backends (either native Python or Node.js).

3. `sacr.config` - This file contains the commands and aliases for use within the current project.  If you are familiar with Node.js then this file is similar to the "scripts" section.

## Configuration
### Defaults (defined with `.sacrrc`)
> [command]
> 
> timeout = 60

If execution will run longer than 60 seconds ensure that this is increased  for your use case.
> [config]
> 
> type = config

If you are using native Python ini files then leave the type as `config`.  If you are leveraging a `package.json` file and wish to continue to do so change the type to `package`.
## Usage
To get usage help run:
> sacr help

If you ran the `init` to generate the defaults then you also got a sample `sacr.config` which looks like this:
> [scripts]
> 
> hello = "echo hello"

If you where to run `sacr run hello` you would get the below output:
> `>` echo hello
>
> hello

## sacr.config Advanced Example
Below is a robust usage sample of sacr from another solution.
<details>

```
[scripts]

###############################################################################
# Audit
###############################################################################
audit = "sacr run audit:pip"
audit:pip = "safety check --full-report"


###############################################################################
# Build
###############################################################################
clean = [
        "sacr clean dist src/shapeandshare_fingerprint_dataset.egg-info **/__pycache__ .coverage coverage.xml htmlcov"
    ]
prebuild = [
    "pip install -r ./requirements.build.txt",
    "pip install -r ./requirements.test.txt",
    "pip install -r ./requirements.txt"
    ]
build = "python -m build"


###############################################################################
# Linting
###############################################################################
lint = [
        "sacr run lint:pylint:check",
        "sacr run lint:isort:check",
        "sacr run lint:black:check"
    ]
lint:pylint:check = "pylint src"
lint:isort:check = "isort --check --diff ."
lint:black:check = "black --line-length=120 --target-version=py310 --check --diff ."
lint:fix = "sacr run lint:isort:fix && sacr run lint:black:fix"
lint:isort:fix = "isort ."
lint:black:fix = "black --line-length=120 --target-version=py310 ."


###############################################################################
# Tests and Coverage
###############################################################################
test = "sacr run test:unit && sacr run coverage"
test:unit = "python test/unit/setup.py"
coverage = [
        "sacr run coverage:report",
        "sacr run coverage:report:html",
        "sacr run coverage:report:xml"
    ]
coverage:report = "coverage report"
coverage:report:html = "coverage html"
coverage:report:xml = "coverage xml"
```
</details>

## TODO
There is always more to do. :)
- [] Test coverage
- [] Move to fire for cli parsing
