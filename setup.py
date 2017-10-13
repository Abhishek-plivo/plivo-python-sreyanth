from setuptools import setup

description = '''\
Plivo Python SDK
----------------

DESCRIPTION
The Plivo Python SDK makes it simpler to integrate communications into your
Python applications using the Plivo REST API.

See https://github.com/plivo/plivo-python for more information.

LICENSE
The Plivo Python SDK is distributed under the MIT License.
'''

setup(
    name='plivo',
    version='4.0.0',
    description='Plivo API client and Plivo XML generator',
    author='Plivo',
    author_email='sdks@plivo.com',
    url='https://github.com/plivo/plivo-python',
    keywords=['plivo', 'plivo xml'],
    long_description=description,
    license='MIT',
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
    ],
    install_requires=[
        'requests >= 2, < 3',
        'six >= 1, < 2',
        'decorator >= 4, < 5',
        'lxml >= 3, < 4',
    ])
