from setuptools import setup, find_packages

setup(
    name="pytestflow",  # Your package name
    version="0.1.0",  # Package version
    packages=find_packages(),  # Automatically find and include package
    install_requires=[],  # Dependencies (list any required packages here)
    author="Uday",
    author_email="billaudaykiran@gmail.com",
    description="A sample pip-installable package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",  # Repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
)
