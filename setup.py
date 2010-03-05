from setuptools import setup, find_packages
import sys, os

install_requires = ['PasteDeploy']
if sys.version_info[:2] < (2, 6):
    install_requires += ['multiprocessing']

version = '0.1'

setup(name='ReloadWSGI',
      version=version,
      description="Robust WSGI auto-reloading for development.",
      long_description="""\

Reload a WSGI application on source change. Keep the old code alive
when the change has syntax errors. Never close the socket, never refuse
a connection.

Replacement for 'paster serve --reload config.ini'.


PID 4197 notifies us of a change in quux.py ::

    quux.py changed; reloading...
    {'status': 'changed', 'pid': 4197}


Oh no! We accidentally typed "foobar" instead of "import foobar"! ::

    Process Process-4:
    Traceback (most recent call last):
     ...
      File "quux.py", line 6, in <module>
        foobar
    NameError: name 'foobar' is not defined


Can we visit our site? YES!::

    127.0.0.1 - - [03/Mar/2010 09:41:52] "GET /orders HTTP/1.1" 200 2345


PID 4197 notifies us of /another/ change in quux.py ::

    quux.py changed; reloading...
    {'status': 'changed', 'pid': 4197}


We've fixed our problem. Once the new process loads, the old process
quits silently ::

    09:42:39,789 DEBUG [quux.run] App started.
    {'status': 'loaded', 'pid': 4354}
              
      """,
      classifiers=[
          "Intended Audience :: Developers",
          "Topic :: Internet :: WWW/HTTP :: WSGI",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          ],
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
      [console_scripts]
      reloadwsgi = reloadwsgi:main
      """,
      )
