from setuptools import setup, find_packages
from os import path
with open("requirements.txt") as fh:
    requirements = fh.read().split("\n")

setup(
    name='politely',
    version='v2.6',
    description='A Korean politeness styler',
    author='Eu-Bin KIM',
    python_requires='>=3.8',
    author_email='tlrndk123@gmail.com',
    license='MIT LICENSE',
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        'politely': [path.join('resources', 'honorifics.yaml'),
                     path.join('resources', 'rules.yaml')]
    }
)
