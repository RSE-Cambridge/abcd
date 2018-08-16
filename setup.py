from setuptools import setup

setup(
        name='abcd',
        version='0.1',
        packages=['abcd'],
        install_requires=['psycopg2-binary', 'pandas', 'ply', 'ase'],
        entry_points={'console_scripts': ['abcd = abcd.__main__:main']}
        )
