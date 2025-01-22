from setuptools import setup
  
setup( 
    name='wrman', 
    version='1.0', 
    description='Maps wiring connections', 
    author='Michael Campos', 
    author_email='michael_c55@berkeley.edu', 
    install_requires=[ 
        'hydra-core', 
        'pandas',
        'natsort' 
    ], 
) 