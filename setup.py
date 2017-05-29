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
  name = 'fca',
  packages = ['fca', 'fca.algorithms', 'fca.algorithms.addIntent', 'fca.defs', 'fca.reader'],
  version = '0.4',
  description = 'A library to implement FCA tools',
  author = 'Victor Codocedo',
  author_email = 'victor.codocedo@gmail.com',
  url = 'https://github.com/codocedo/fca',
  download_url = 'https://github.com/codocedo/fca/archive/0.4.tar.gz',
  keywords = ['formal concept analysis', 'pattern mining', 'add intent', 'data mining'],
  classifiers = [],
)