# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from setuptools import setup, find_packages
import os

version = '1.0'

tests_require = [
    'infrae.testing',
    ]

setup(name='infrae.scales',
      version=version,
      description="WSGI middleware for scales",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Zope Public License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Zope2",
          ],
      keywords='zope2 wsgi silva infrae',
      author='Sylvain Viollon',
      author_email='info@infrae.com',
      url='http://svn.infrae.com/infrae.scales/trunk',
      license='ZPL',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['infrae'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'scales',
        'objgraph',
        'WebOb',
        ],
      entry_points={
        'paste.filter_app_factory': [
            'main = infrae.scales.wsgi:make_middleware',
            ],
        },
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
