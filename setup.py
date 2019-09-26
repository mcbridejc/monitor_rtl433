#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='monitor_rtl433',
      version='1.0',
      description='Python HTTP wrapper for rtl_433',
      author='Jeff McBride',
      author_email='jeff@jeffmcbride.net',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['monitor_rtl433=monitor_rtl433.main:main']
      },
      install_requires=[
         'python-dateutil',
         'flask',
         'flask_table'
      ]
    )

    