from setuptools import setup, find_packages
  
setup( 
    name='wrman', 
    version='0.1', 
    description='Maps wiring connections', 
    author='Michael Campos', 
    author_email='michael_c55@berkeley.edu', 
    packages=find_packages(include=['wrman', 'wrman.*']), 
    install_requires=[ 
        'hydra-core', 
        'pandas',
        'natsort' 
    ], 
) 