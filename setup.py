from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='Sparkler',
      version=version,
      description="A Spark API client written in Python",
      long_description="""\
A Spark API client written in Python""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='spark sparkapi',
      author='Joshua Murray',
      author_email='joshua.murray@gmail.com',
      url='http://www.github.com/joshcom/sparkler',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples','tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
