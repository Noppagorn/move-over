from setuptools import setup, find_packages

setup(
    name="cows-detector-database",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "firebase-admin",
        "termcolor",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    author="Tong",
    author_email="your.email@example.com",
    description="Database utilities for Cows Detector project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cows-detector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 