from setuptools import find_packages, setup

long_description = '''\
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
    version='4.0.0b1',
    description='Plivo API client and Plivo XML generator',
    long_description=long_description,
    url='https://github.com/plivo/plivo-python',
    author='The Plivo SDKs Team',
    author_email='sdks@plivo.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Telephony',
    ],
    install_requires=[
        'requests >= 2, < 3',
        'six >= 1, < 2',
        'decorator >= 4, < 5',
        'lxml >= 3, < 4',
    ],
    keywords=['plivo', 'plivo xml', 'voice calls', 'sms'],
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'tests.*']), )
