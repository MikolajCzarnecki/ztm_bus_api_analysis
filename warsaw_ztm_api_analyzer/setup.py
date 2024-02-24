from setuptools import setup

setup(
    name='warsaw_ztm_api_analyzer',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/shuds13/pyexample',
    author='Mikolaj Czarnecki',
    author_email='mc448206@students.mimuw.edu.pl',
    license='MIT',
    packages=['analyzer', 'scrapper'],
    install_requires=['pandas',
                      'numpy', 
                      'datetime',
                      'matplotlib'                    
                      ]
)