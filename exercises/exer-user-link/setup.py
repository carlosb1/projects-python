""" Setup configuration """
from setuptools import find_packages, setup

dependencies = [
    'faker==6.5.0',
    'atomicwrites==1.4.0',
    'attrs==20.3.0',
    'backcall==0.2.0',
    'cffi==1.14.5',
    'cryptography==3.4.6',
    'decorator==4.4.2',
    'Flask==1.1.2',
    'itsdangerous==1.1.0',
    'jedi==0.18.0',
    'Jinja2==2.11.3',
    'MarkupSafe==1.1.1',
    'mccabe==0.6.1',
    'more-itertools==8.7.0',
    'packaging==20.9',
    'parso==0.8.1',
    'pexpect==4.8.0',
    'pickleshare==0.7.5',
    'pluggy==0.13.1',
    'ptyprocess==0.7.0',
    'py==1.10.0',
    'pycparser==2.20',
    'pyflakes==2.2.0',
    'Pygments==2.8.0',
    'pyparsing==2.4.7',
    'snowballstemmer==2.1.0',
    'traitlets==5.0.5',
    'typed-ast==1.4.2',
    'typing-extensions==3.7.4.3',
    'wcwidth==0.2.5',
    'Werkzeug==1.0.1',
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
    name='searchfile',
    version='0.1.0',
    url='https://github.com/carlosb1/exer-user-link',
    license='BSD',
    author='Carlos Baez',
    author_email='carlos.baezruiz@gmail.com',
    description='Exercise for user link',
    long_description=__doc__,
    packages=find_packages(exclude=['test_*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    extras_require=dict(test=test_dependencies),
    entry_points={
        'console_scripts': [
            'user-link = exer_user_link.app:main',
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
