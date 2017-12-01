# pnglatex
pnglatex, a small program that converts LaTeX snippets to png

## Requiremens

[Python3](https://www.python.org/downloads/)

A LaTeX distribution such as [TeX Live](https://www.tug.org/texlive/) or [MiKTeX](https://miktex.org/)

`pdfcrop, pnmtopng, pdftoppm` You should be able to find those programs in your distro package manager or [Homebrew](https://brew.sh/)

`pnmtopng` can be typically found in the package `netpbm`

`pdftoppm` can be typically found in the package `poppler-utils`

## Install

In your terminal, type:
```
pip install pnglatex
```
On some systems you might need to use `pip3` instead of `pip`

## Usage

pnglatex comes with a simple command line interface.

To use the cli, you can check the help message using:
```
pnglatex -h
```

Here's the help message in full:
```
usage: pnglatex.py [-h] -c "LaTeX string" [-o filename]

pnglatex, a small program that converts latex snippets to png

optional arguments:
  -h, --help         show this help message and exit
  -c "LaTeX string"  The LaTeX string to convert
  -o filename        The output filename.
```

Some examples:

`pnglatex -c "\[\frac{1}{2}\]"`, `pnglatex -c foo -o foo.png`

pnglatex also includes a single function that you can include in your code.

Here's its docstring in full:
```python
def pnglatex(tex_string, output=None):
    """
    Produce an png based on a input LaTeX snippet.

    @param tex_string: The LaTeX string.
    @param output: The output filename. It can also be a pathlib.Path object.
                   If not provided, this will be randomly generated.

    @return: A Path object of the output file
    @raises ValueError: If the input is empty of something went wrong with
                        the image creation.
    """
```

An example usage would be:
```python
from pnglatex import pnglatex

output = pnglatex(r'\[\displaystyle{\sum_{i=0}^{10} 3i}\]', 'output.png')
```

## Licence

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

See [LICENSE](LICENSE) for details.
