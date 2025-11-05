"""Setup script for gmail-to-notebooklm package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="gmail-to-notebooklm",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Convert Gmail emails from a label into Markdown files for Google NotebookLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gmail-to-notebooklm",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.9",
    install_requires=[
        "google-api-python-client>=2.100.0,<3.0.0",
        "google-auth>=2.25.0,<3.0.0",
        "google-auth-oauthlib>=1.2.0,<2.0.0",
        "google-auth-httplib2>=0.2.0,<1.0.0",
        "beautifulsoup4>=4.12.0,<5.0.0",
        "lxml>=4.9.0,<6.0.0",
        "html2text>=2024.2.0",
        "click>=8.1.0,<9.0.0",
        "python-dateutil>=2.8.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gmail-to-notebooklm=gmail_to_notebooklm.main:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="gmail markdown notebooklm email converter",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gmail-to-notebooklm/issues",
        "Source": "https://github.com/yourusername/gmail-to-notebooklm",
        "Documentation": "https://github.com/yourusername/gmail-to-notebooklm#readme",
    },
)
