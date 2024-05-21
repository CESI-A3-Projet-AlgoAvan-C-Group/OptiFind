from setuptools import setup, find_packages

setup(
    name='OptiFind_app',
    version='0.1',
    packages=find_packages(),
    insall_requires=[
        'flask',
        'geojson',
    ],)