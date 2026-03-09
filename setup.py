"""Setup script for the Python Cheatsheet MCP server."""

from setuptools import find_packages, setup

setup(
    name='python-cheatsheet-mcp',
    version='1.0.0',
    description='MCP server for the Comprehensive Python Cheatsheet',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests*']),    install_requires=[
        'mcp>=1.0.0',
        'pydantic>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'python-cheatsheet-mcp=run_mcp_server:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
