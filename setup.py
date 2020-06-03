from keep import __version__

from setuptools import setup, find_packages

install_requirements = [
    'gkeepapi>=0.11.16',
    'pyfiglet>=0.8.post1',
    'PyInquirer>=1.0.3',
    'argparse>=1.4.0',
    'keyring>=21.2.1',
    'keyrings.alt>=3.4.0'
]

setup(
    name='keep-cli',
    version=__version__,
    author='Zachary Ashen',
    author_email='zachary.h.a@gmail.com',
    license='MIT',
    description='Keep-cli is a cli Google Keep client. You can add, delete, and manage your Google Keep notes.',
    url='https://github.com/zack-ashen/keep-cli',
    long_description=open('README-pip.md').read(),
    long_description_content_type ="text/markdown",
    install_requires=install_requirements,
    python_requires=">=3",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='cli google notes notetaking todo google-keep keep keep-cli',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'keep=keep.keep:main',
            'keep-cli=keep.keep:main'
        ]
    }
)
