from setuptools import setup, find_packages
import os

version = '0.8b2'

setup(name='collective.logbook',
      version=version,
      description="Advanced Persistent Error Log",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ramon Bartl',
      author_email='ramon.bartl@nexiles.de',
      url='https://svn.plone.org/svn/collective/collective.logbook',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
      ],
      extras_require={
          'test': [
               'plone.app.testing',
               'unittest2',
           ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
