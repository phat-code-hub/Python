from setuptools import setup,find_packages
import portalocker
setup(
    name='Cmath',
    version='0.2',
    # packages=['Cmath'],
    packages=find_packages(where='Cmath'),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'Cmath  = Cmath:Add',
        ],
    },
)