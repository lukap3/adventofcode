# adventofcode
Advent Of Code python solutions

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Environment Setup](#environment-setup)
  - [Running](#running)

## Introduction
This Python project is designed to tackle the challenges presented in the Advent of Code event.

## Getting Started

### Prerequisites
- Python 3.x
- Pipenv

### Installation
1. Install dependencies using Pipenv:
```bash
pipenv install
```

## Usage

### Environment setup
Before using the project, you need to set up the environment variables.

````bash
cp .envrc-TEMPLATE .envrc
direnv allow
````

Set the `YEAR` and `AOC_SESSION` variables.
You can get the `AOC_SESSION` from the cookie on the advent of code page.

### Running

To fetch the instructions for a new day run:
```bash
make new
```

And to update the instructions for part 2 after submitting part 1 run:
```bash
make update-last
```

- The instructions will be added to `<YEAR>/data/dayX/instructions.md`
- The input data will be added to `<YEAR>/data/dayX/data.txt`
- An example data file will be generated: `<YEAR>/data/dayX/example.txt`
- A new python file will be generated: `<YEAR>/days/dayX.py`

Configure the tests by editing the `test_files` dict:
```python
test_files = {
  "data/dayX/example.txt": [
    "part1_example_solution",
    "part2_example_solution"
    ]
}
```

Add your logic to `part_1_logic` and `part_2_logic` methods.

The inputs from `<YEAR>/days/dayX/example.txt` and `<YEAR>/days/dayX/data.txt` are passed to the `part_X_logic` functions.
The challenges usually require you to split the input by lines and split the lines by a specific character or something similar.
Add that logic to the `parse_file` method.

By running the `dayX.py` file directly or by using `make run-last` the code will first be run using the example
input and checked if it results in the expected solutions provided in the `test_files` dict.
