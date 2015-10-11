try:
    from setuptool import setuptool
except ImportError:
    from distutils.core import setuptool

config = {
    'description': 'Game Lexicon',
    'author': 'Rogier Schaap',
    'url' : 'URL to get it at',
    'download_url': 'Where to download it',
    'author_email': 'reschaap@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ex48'],
    'scripts': [],
    'name': 'ex48',
}

setup(**config)