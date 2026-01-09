from setuptools import setup, find_packages

setup(
    name="csim",
    version="1.1.2",
    packages=find_packages(),
    install_requires=[
        "antlr4-python3-runtime",
        "zss",
    ],
    author="Eddy Lecoña",
    author_email="crew0eddy@gmail.com",
    description="Code Similarity (csim) is a method designed to detect similarity between source codes",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/EdsonEddy/csim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    keywords="code analysis, similarity detection, tree parser, tree edit distance, code snippets, code comparison",
    project_urls={
        "Bug Tracker": "https://github.com/EdsonEddy/csim/issues",
        "Documentation": "https://github.com/EdsonEddy/csim/wiki",
        "Source Code": "https://github.com/EdsonEddy/csim",
    },
    python_requires='>=3.9',
    platforms=["All"],
    entry_points={
        'console_scripts': [
            'csim=csim.main:main',
        ],
    },
    license="MIT",
)