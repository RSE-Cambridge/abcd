from setuptools import setup

setup(
        name='abcd',
        version='0.1',
        packages=['abcd'],
        scripts=['abcd.py'],
        install_requires=['psycopg2-binary', 'pandas', 'ply', 'ase']
        )
