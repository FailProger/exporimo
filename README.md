# Exporimo

## About
**Library for fast expose <code>marimo</code> notebook to Internet.**

Use <code>exporimo</code> you can start <code>marimo</code> on you computer and expose it for using from anywhere,
for example by your smartphone.

**It is not official additional for <code>marimo</code>!**


## Installation
You can install <code>exporimo</code> from PyPI:

    pip install exporimo


## Example
Example code of <code>exporimo</code> using:

    from exposrimo import Exporimo

    
    # Start and expose marimo
    Exporimo.start_marimo("edit", "main.py")
    Exporimo.wait()  # Don`t stop programm until marimo work or until input in terminal "stop"


## Warning
**I am not marimo developer.** **It is not official additional for <code>marimo</code>!**

Url to <code>marimo</code> github: https://github.com/marimo-team/marimo


## License
<code>Exporimo</code> if offered under the MIT license. More see LICENSE file.
