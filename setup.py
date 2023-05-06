from setuptools import setup

setup(
    name='graph_drawing',
    version='0.1',
    install_requires=[
        'networkx',
        'matplotlib',
        'argparse',
        'tabulate',
        'imageio',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'graph_drawing = main.main:main'
        ]
    }
)
