from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='kawasemi',
    version='0.1.0',
    license='MIT License',
    description='A library for generating a LANGUAGE object for a input statute in Japanese',
    author='Suguru Matsuyoshi',
    url='https://github.com/uuu-CL/kawasemi',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov']
)
