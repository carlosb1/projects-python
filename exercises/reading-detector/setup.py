"""
Exercise for HolaLuz for a fraud reading detector
"""
from setuptools import find_packages, setup

dependencies = [
    'click==7.1.2',
    'pandas==0.25.1',
    'numpy==1.16.2',
    'tabulate==0.8.7'
]

test_dependencies = [
    'pytest==5.1.2',
    'pytest-cov==2.7.1',
    'pytest-flake8==1.0.6',
    'pytest-mypy==0.4.0',
    'pydocstyle==4.0.1',
    'pep8-naming==0.8.1',
    'pytest-docstyle==2.0.0',
    'flake8 == 3.8.1',
]


setup(
    name='readingdetector',
    version='0.1.0',
    url='https://github.com/carlosb1/reading-detector',
    license='BSD',
    author='Carlos Baez',
    author_email='carlos.baezruiz@gmail.com',
    description='Exercise for HolaLuz for a fraud reading detector',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    extras_require=dict(test=test_dependencies),
    entry_points={
        'console_scripts': [
            'reading-detector = reading_detector.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
