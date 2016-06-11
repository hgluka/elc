try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A programming language based on the lambda calculus',
    'author':'lucantrop',
    'url':'github.com/lucantrop/elc',
    'version':'0.1',
    'install_requires': ['nose'],
    'packages': ['elc'],
    'scripts': [],
    'name': 'elc'
}

setup(**config)
