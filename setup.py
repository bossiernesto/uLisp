from setuptools import setup, find_packages

setup(name="uLisp",
    version="0.1.2",
    description="Very tiny Lisp interpreter",
    author="Ernesto Bossi",
    author_email="bossi.ernestog@gmail.com",
    url="",
    license="BSD",
    py_modules=find_packages(exclude=('test')),
    keywords="Interpreter Lisp",
    classifiers=["Development Status :: 2 - Pre-Alpha",
                 "Environment :: Console",
                 "Topic :: Software Development :: Interpreters",
                 "License :: OSI Approved :: BSD License"]
)
