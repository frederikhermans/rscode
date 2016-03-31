import setuptools
from setuptools import Extension
import distutils.command.build_ext

setuptools.setup(name='rscode',
                 version='1.0a',
                 packages=setuptools.find_packages(),
                 ext_modules=[Extension('rscode.reed_solomon',
                                        ['c-src/reed_solomon.c'],
                                        libraries=['m'])],
                 author='Frederik Hermans',
                 license='GPL3',
                 url='https://github.com/frederikhermans/rscode',
                 cmdclass={'build_ext': distutils.command.build_ext.build_ext},
                 install_requires=['numpy'])
