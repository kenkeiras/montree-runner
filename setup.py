#!/usr/bin/env python3

from setuptools import setup

setup(name='montree-runner',
      version='0.1',
      description='Python runner for tests defined on MonTree.',
      url='https://github.com/kenkeiras/montree-runner',
      author='kenkeiras',
      author_email='kenkeiras@codigoparallevar.com',
      license='MIT',
      packages=['montree-runner'],
      scripts=['bin/montree-runner'],
      include_package_data=True,
      install_requires = ['requests'],
zip_safe=False)
