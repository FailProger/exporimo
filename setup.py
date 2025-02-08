from setuptools import setup, find_packages


__version__ = "0.1.2"

with open("README.md", "r", encoding="UTF-8") as file:
    long_description = file.read()

requires_list = [
    "marimo>=0.10.0",
    "netifaces>=0.11.0"
]

setup(
    name="exporimo",
    version=__version__,
    author="Vyacheslav Pervakov",
    author_email="WsrrcalzWehgwmD@protonmail.com",
    description="Library for fast expose marimo notebook to Internet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FailProger/exporimo.git",
    project_urls={
        "GitHub": "https://github.com/FailProger/exporimo.git",
        "PyPI": "https://pypi.org/project/exporimo/"
    },
    license="MIT License",
    license_file="LICENSE",
    keywords=["Python", "marimo"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    packages=find_packages(),
    python_requires = ">=3.9",
    install_requires=requires_list
)
