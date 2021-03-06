import setuptools

f = open('README.md', 'r')
long_description = f.read()
f.close()

setuptools.setup(
    name="cati",
    version="0.1-alpha3",
    author="parsa shahmaleki",
    author_email="parsampsh@gmail.com",
    description="The Cati Unix Package manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parsampsh/gameoflife",
    packages=setuptools.find_packages(),
    scripts=['etc/bin/cati'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
    install_requires=[
        'packaging >= 20.4',
        'requests >= 2.25.0',
        'wget >= 3.2',
    ],
)
