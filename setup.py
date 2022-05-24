"""
FCA - Python libraries to support FCA tasks
Copyright (C) 2017  Victor Codocedo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.core import setup

setup(
    name='fca',
    packages=[
        'fca',
        'fca.algorithms',
        'fca.algorithms.addIntent',
        'fca.algorithms.cbo',
        'fca.algorithms.lecenum_closures',
        'fca.algorithms.lexenum_closures',
        'fca.algorithms.pre_closure',
        'fca.algorithms.canonical_base',
        'fca.defs.patterns',
        'fca.defs.patterns.hypergraphs',
        'fca.defs',
        'fca.io',
        'fca.io.file_models',
        'fca.io.input_models',
        'fca.io.sorters',
        'fca.io.transformers'
        ],
    version='3.2',
    description='A library to implement Formal Concept Analysis tasks and other tools',
    author='Victor Codocedo',
    author_email='victor.codocedo@gmail.com',
    url='https://github.com/codocedo/fca',
    download_url='https://github.com/codocedo/fca/archive/3.2.tar.gz',
    keywords=[
        'formal concept analysis',
        'pattern mining',
        'add intent',
        'data mining',
        'close by one',
        'cbo',
        'pattern structures',
        'interval pattern mining'
        ],
    classifiers=[],
    install_requires=[
        "enum34"
        ]
    )
