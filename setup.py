from setuptools import setup, find_packages

setup(name='featurematrix',
      version='0.1',
      packages=find_packages(),
      scripts=['bin/ftmtx.py',
               'bin/ftmtx_combine.py',
               'bin/txt2features.py',
               'bin/ftsearch.py']
)
