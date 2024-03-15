#!/usr/bin/env python

import setuptools

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setuptools.setup(
    name='strider',
    version='0.1.0',
    license='BSD',
    author='strider',
    author_email='author@example.com',
    description="File system navigator.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['xonsh[full]'],
    scripts=['strider/strider'],
    packages=['xontrib'],
    package_data={'strider': ['*.py'], 'xontrib': ['*.py', '*.xsh']},
    platforms='any',
    url='https://github.com/strider/strider',
    project_urls={
        "Documentation": "https://github.com/anki-code/strider/blob/master/README.md",
        "Code": "https://github.com/anki-code/strider",
        "Issue tracker": "https://github.com/anki-code/strider/issues",
    },
    classifiers=[
        "License :: OSI Approved :: BSD License"
    ]
)
