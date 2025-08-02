#!/usr/bin/env python3
"""
Setup script for PDF Document Translator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf-document-translator",
    version="1.0.0",
    author="PDF Translator Team",
    description="Translate PDF documents using LibreTranslate while preserving formatting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pdf-document-translator",
    py_modules=["pdf_translator"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf-translator=pdf_translator:main",
        ],
    },
)