from setuptools import setup, find_packages
from mksaltformula import __version__

setup(
  name='mksaltformula',
  version=__version__,
  packages=find_packages(exclude='tests'),
  test_suite='tests',
  entry_points={
    'console_scripts': [ 'mksaltformula = mksaltformula:main'  ]
  },
)
