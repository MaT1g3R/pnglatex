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
from sys import stderr
from os import devnull
from subprocess import Popen, PIPE
from contextlib import contextmanager
from string import digits, ascii_letters
from pathlib import Path
from shutil import which
from argparse import ArgumentParser
from random import choice


__all__ = ['pnglatex']


_BINARIES = ('pdflatex', 'pdfcrop', 'pdf2ppm', 'pnm2png')
_TEX_BP = """\\documentclass{{article}}
\\thispagestyle{{empty}}
\\begin{{document}}
{}
\\end{{document}}"""


def _get_bin(name):
    """
    Get the executable name of a program based on different OS.
    """
    res = which(name)
    if '2' in name and not res:
        res = which(name.replace('2', 'to'))
    if not res:
        raise ValueError('Eexecutable {} not found'.format(name))
    return res


def _get_fname():
    """
    Get a random file name that does not exist in the current directory.
    """
    name = ''.join(choice(digits + ascii_letters) for _ in range(6))
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


def _run(tex_string, jobname, output, null, binaries):
    """
    Run the tex string through some processes to produce a png at output.

    Returns the exit status of pnm2png
    """
    pdflatex, pdfcrop, pdf2ppm, pnm2png = binaries

    def popen(*args, stdin=None, out=null, err=null):
        return Popen(args, stdin=stdin, stdout=out, stderr=err)

    with popen(pdflatex, '-jobname=' + jobname, stdin=PIPE) as pdflatex_p:
        pdflatex_p.communicate(input=tex_string.encode(encoding='UTF-8'))

    with popen(pdfcrop, jobname + '.pdf') as crop:
        crop.wait()

    with open(output, 'wb+') as f,\
        popen(pdf2ppm, jobname + '-crop.pdf', out=PIPE) as ppm,\
            popen(pnm2png, stdin=ppm.stdout, out=f) as png:
        png.wait()
        return png.poll()


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
    if not tex_string:
        raise ValueError("LaTeX expression cannot be empty!")
    jobname = _get_fname()
    output = output or jobname + '.png'
    tex_string = _TEX_BP.format(tex_string)
    binaries = tuple(_get_bin(b) for b in _BINARIES)

    with _cleanup(jobname), open(devnull, 'w') as null:
        status = _run(tex_string, jobname, output, null, binaries)

    if status != 0:
        with Path(output) as o:
            try:
                o.unlink()
            except FileNotFoundError:
                pass
        raise ValueError("Failed to generate png file.")
    return Path(output)


def main():
    """
    Program entry point when ran as a script.
    """
    des = 'pnglatex, a small program that converts latex snippets to png'
    parser = ArgumentParser(description=des)
    parser.add_argument('-c', help='The LaTeX string to convert',
                        required=True, metavar='"LaTeX string"')
    parser.add_argument('-o', help='The output filename.', metavar='filename')
    args = parser.parse_args()
    try:
        out = pnglatex(args.c, args.o)
    except ValueError as e:
        print(e, file=stderr)
        exit(1)
    else:
        print('Success! Your file has been saved at {}'.format(out))


if __name__ == '__main__':
    main()
