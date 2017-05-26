from distutils.core import setup
setup(
  name = 'fca',
  packages = ['fca', 'fca.algorithms', 'fca.algorithms.addIntent', 'fca.defs', 'fca.reader'], # this must be the same as the name above
  version = '0.2',
  description = 'A library to implement FCA tools',
  author = 'Victor Codocedo',
  author_email = 'victor.codocedo@gmail.com',
  url = 'https://github.com/codocedo/fca',
  download_url = 'https://github.com/codocedo/fca/archive/0.2.tar.gz',
  keywords = ['formal concept analysis', 'pattern mining', 'add intent', 'data mining'],
  classifiers = [],
)