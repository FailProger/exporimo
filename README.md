# Exporimo

## About
**Library for fast expose marimo notebook to Internet.**

Use <code>exporimo</code> you can start marimo on you computer and expose it for using from anywhere,
for example by your smartphone.


## Installation
You can install <code>exporimo</code> from PyPI:

    pip install exporimo

## Example
Example code of <code>exporimo</code> using:

    from exposrimo import Exporimo

    
    # Start and expose marimo
    Exporimo.start_marimo("edit", "main.py")
    Exporimo.wait()  # Don`t stop programm until marimo work or until input in terminal "stop"


# License
<code>Exporimo</code> if offered under the MIT license. More see LICENSE file.
