from setuptools import setup 
  
setup( 
    name='wrman', 
    version='0.1', 
    description='Maps wiring connections', 
    author='Michael Campos', 
    author_email='michael_c55@berkeley.edu', 
    packages=['my_package'], 
    install_requires=[ 
        'hydra-core', 
        'pandas',
        'natsort' 
    ], 
) 