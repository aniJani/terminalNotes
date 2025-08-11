from setuptools import setup, find_packages

setup(
    name="terminal-notes",
    version="1.0.0",
    description="A beautiful and powerful notes application in your terminal",
    author="Your Name",
    py_modules=["notes"],
    python_requires=">=3.7",
    install_requires=[
        "typer>=0.16.0",
        "rich>=14.1.0",
    ],
    entry_points={
        "console_scripts": [
            "notes=notes:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
