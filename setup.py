import setuptools
import subprocess
import distutils.command.build_py


class BuildWithMake(distutils.command.build_py.build_py):
    def run(self):
        subprocess.check_call(['make', '-C', 'c-src'])
        distutils.command.build_py.build_py.run(self)


setuptools.setup(name='rscode',
                 version='1.0a',
                 packages=setuptools.find_packages(),
                 author='Frederik Hermans',
                 license='GPL3',
                 cmdclass={'build_py': BuildWithMake},
                 url='https://github.com/frederikhermans/rscode')
