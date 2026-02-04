from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    description="Maze generation package for 42 project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
)
