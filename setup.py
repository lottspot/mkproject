from setuptools import setup, find_packages
from mkproject import __version__

setup(
  name='mkproject',
  version=__version__,
  packages=find_packages(exclude='tests'),
  test_suite='tests',
  entry_points={
    'console_scripts': [ 'mkproject = mkproject:main'  ]
  },
)
