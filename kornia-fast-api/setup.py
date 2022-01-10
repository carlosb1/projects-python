from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='kornia-api',
    version='0.1.0',
    description='Kornia Fast API',
    author='Carlos Baez',
    author_email='carlos.baezruiz@gmail.com',
    url='https://kornia.io',
    packages=find_packages(include=['kornia_api', 'kornia_api.*']),
    install_requires=required,
    # extras_require={'plotting': ['matplotlib>=2.2.0', 'jupyter']},
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['kornia-api=kornia_api.main:run']
    },
    # package_data={'exampleproject': ['data/schema.json']}
)
