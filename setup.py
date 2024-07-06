from setuptools import setup, find_packages

setup(
    name='ClaudeCoder',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'anthropic',
        'pydantic',
        'python-dotenv',
        'sqlite3'
    ],
)
