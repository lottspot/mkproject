from setuptools import setup, find_packages
from mkproject import __version__, __pkg__

setup(
  name=__pkg__,
  version=__version__,
  packages=find_packages(exclude='tests'),
  test_suite='tests',
  entry_points={
    'console_scripts': [ '{} = {}:main'.format(__pkg__, __pkg__)  ]
  },
)
