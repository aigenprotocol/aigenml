from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="aigenml",
    version="0.01",
    license='MIT',
    author="Aigen Protocol",
    author_email='kailash@aigenprotocol.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aigenprotocol/aigenml',
    keywords='Aigen machine learning libray',
    install_requires=[
        "tensorflow==2.11.0",
        "pandas",
        "flask",
        "flask-cors",
        "Flask-SQLAlchemy",
        "Flask-Migrate",
        "SQLAlchemy-serializer"
    ]
)
