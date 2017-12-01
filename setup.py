from re import match
from pathlib import Path

from setuptools import setup, find_packages


HERE = Path(Path(__file__).parent)

META = {}

with (HERE / 'pnglatex' / '__init__.py').open() as init_file:
    for line in init_file:
        matched = match(r"^__(.+)__\s+=\s+'(.+)'$", line.rstrip())
        if not matched:
            continue
        name = matched.group(1)
        if name == 'title':
            name = 'name'
        META[name] = matched.group(2)

setup(
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pnglatex = pnglatex.pnglatex:main']
    },
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
