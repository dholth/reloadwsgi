from setuptools import setup, find_packages
import sys, os

install_requires = ['PasteDeploy']
if sys.version_info[:2] < (2, 6):
    install_requires += ['multiprocessing']

version = '0.0'

setup(name='ReloadWSGI',
      version=version,
      description="Reloading WSGI server for development.",
      long_description="""\
ReloadWSGI watches for changes in your WSGI application, but does not kill
your running application until the new version has loaded successfully.
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wsgi',
      author='Daniel Holth',
      author_email='dholth@fastmail.fm',
      url='',
      license='MIT',
      py_modules=['reloadwsgi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
