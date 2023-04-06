from setuptools import setup

setup(
    name='graph-drawing',
    version='0.1',
    install_requires=[
        'networkx',
        'matplotlib',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'graph-drawing = main.main:main'
        ]
    }
)
