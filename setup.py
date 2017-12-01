#!/usr/bin/env python3
from re import match
from pathlib import Path
from subprocess import Popen
from sys import argv


from setuptools import setup, find_packages


HERE = Path(Path(__file__).parent)
META = {}
PKGDATA = {'': ['LICENSE', 'README.md']}


if argv[-1] == 'publish':
    MAKE = ('python', 'setup.py', 'sdist', 'bdist_wheel')
    UP = ('twine', 'upload', 'dist/*')
    with Popen(MAKE) as m:
        m.wait()
    with Popen(UP) as u:
        u.wait()
    exit(0)


with (HERE / 'pnglatex' / '__init__.py').open() as init_file:
    for line in init_file:
        matched = match(r"^__(.+)__\s+=\s+'(.+)'$", line.rstrip())
        if not matched:
            continue
        name = matched.group(1)
        if name == 'title':
            name = 'name'
        META[name] = matched.group(2)


with (HERE / 'README.md').open() as r:
    README = r.read()


setup(
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pnglatex = pnglatex.pnglatex:main']
    },
    package_data=PKGDATA,
    include_package_data=True,
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Utilities',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Development Status :: 5 - Production/Stable'
    ],
    **META
)
