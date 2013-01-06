from setuptools import setup, find_packages
from trouvailles import __version__


install_requires = ['xappy', 'cornice', 'BeautifulSoup']

try:
    import argparse     # NOQA
except ImportError:
    install_requires.append('argparse')


with open('README.rst') as f:
    README = f.read()


classifiers = ["Programming Language :: Python",
               "License :: OSI Approved :: Apache Software License",
               "Development Status :: 1 - Planning"]


setup(name='trouvailles',
      version=__version__,
      url='https://github.com/tarekziade/trouvailles',
      packages=find_packages(),
      long_description=README,
      description=("Xapian Web Service"),
      author="Tarek Ziade",
      author_email="tarek@ziade.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      trouvailles-serve = trouvailles.server:main
      """)
