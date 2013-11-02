from setuptools import setup, find_packages

setup(name="uLisp",
    version="0.1",
    description="Very tiny Lisp interpreter",
    author="Ernesto Bossi",
    author_email="bossi.ernestog@gmail.com",
    url="",
    license="GPL v3",
    py_modules=find_packages(exclude=('test')),
    keywords="Memory Database",
    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Environment :: Console",
                 "Topic :: Database",
                 "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"]
)
