#!/usr/bin/env python3
"""
pnglatex, a small program that converts latex snippets to png
Copyright (C) 2017 Peijun Ma

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This program can be run directly as a script. It also provides the pnglatex
function which you can import and use in your own programs.
"""

from subprocess import Popen, PIPE
from contextlib import contextmanager
from pathlib import Path
from secrets import token_hex

__all__ = ['pnglatex']


_TEX_BP = """\\documentclass{{article}}
\\thispagestyle{{empty}}
\\begin{{document}}
{}
\\end{{document}}"""


def _get_bin(name):
    """
    Get the executable name of a program based on different OS.
    """
    # TODO: Implement this
    return name


def _get_fname():
    """
    Get a random file name that does not exist in the current directory.
    """
    name = token_hex(6)
    for f in Path('.').iterdir():
        if name in str(f):
            return _get_fname()
    return name


@contextmanager
def _cleanup(jobname):
    """
    Clean up the LaTeX mess after we compiled the tex string.
    """
    yield

    def _cleanup_suffix(suffix):
        with Path(jobname + suffix) as p:
            try:
                p.unlink()
            except FileNotFoundError:
                pass

    for suf in ('.pdf', '.out', '.aux', '.log', '-crop.pdf'):
        _cleanup_suffix(suf)


def _run(tex_string, jobname, output):
    """
    Run the tex string through some processes to produce a png at output.

    Returns the exit status of pnm2png
    """
    with Popen((_get_bin('pdflatex'), f'-jobname={jobname}'),
               stdin=PIPE) as proc:
        proc.communicate(input=tex_string.encode(encoding='UTF-8'))

    with Popen((_get_bin('pdfcrop'), f'{jobname}.pdf')) as crop:
        crop.wait()

    with open(output, 'wb+') as f,\
        Popen((_get_bin('pdftoppm'), f'{jobname}-crop.pdf'), stdout=PIPE)\
        as pdftoppm,\
            Popen((_get_bin('pnm2png'),), stdin=pdftoppm.stdout, stdout=f)\
            as pnm2png:
        pnm2png.wait()
        status = pnm2png.poll()
    return status


def pnglatex(tex_string, output=None):
    """
    Produce an png based on a input LaTeX snippet.

    @param tex_string: The LaTeX string.
    @param output: The output filename. It can also be a pathlib.Path object.
                   If not provided, this will be randomly generated.

    @raises ValueError: If the input is empty of something went wrong with
                        the image creation.
    """
    if not tex_string:
        raise ValueError("LaTeX expression cannot be empty!")
    jobname = _get_fname()
    output = output or jobname + '.png'
    tex_string = _TEX_BP.format(tex_string)
    with _cleanup(jobname):
        status = _run(tex_string, jobname, output)
    if status != 0:
        with Path(output) as o:
            try:
                o.unlink()
            except FileNotFoundError:
                pass
        raise ValueError("Failed to generate png file.")


def main():
    """
    Program entry point when ran as a script.
    """
    # TODO: Implement this
    pass


if __name__ == '__main__':
    main()
