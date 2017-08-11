from setuptools import setup
import os

ROOT_DIR='pymkbdypts'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(name='pymkbdypts',
      version=version,
      description='Parses open boundary information in combination with a given topography for a GETM (General Estuarine transport model, www.getm.eu) setup',
      url='https://github.com/pholter/pymkbdypts',
      author='Peter Holtermann',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['pymkbdypts'],
      scripts = [],
      entry_points={'console_scripts': ['pymkbdypts=pymkbdypts.pymkbdypts:__main__'], },      
      package_data = {'':['VERSION']},
      zip_safe=False)
