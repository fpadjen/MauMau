try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Kleines MauMau-Spiel',
    'author': 'Frederik',
    'url': '',
    'download_url': '',
    'author_email': 'code@padjen.de',
    'version': '0.0.1',
    'install_requires': ['nose'],
    'packages': ['maumau'],
    'scripts': [],
    'name': 'maumau'
}

setup(**config)
