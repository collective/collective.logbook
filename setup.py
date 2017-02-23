# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '0.9.0'

long_description = (
    open('README.rst').read() +
    '\n' +
    open(os.path.join('docs', 'HISTORY.txt')).read() +
    '\n')

setup(name='collective.logbook',
      version=version,
      description="Advanced Persistent Error Log",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Ramon Bartl',
      author_email='rb@ridingbytes.com',
      url='https://github.com/collective/collective.logbook',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'unittest2',
              'robotsuite',
              'robotframework-selenium2library',
              'plone.app.robotframework',
              'robotframework-debuglibrary',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
