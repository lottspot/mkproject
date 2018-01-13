from setuptools import setup, find_packages

setup(
  name='mksaltformula',
  version='0.0.0',
  packages=find_packages(exclude='tests'),
  test_suite='tests',
  entry_points={
    'console_scripts': [ 'mksaltformula = mksaltformula:main'  ]
  },
)
