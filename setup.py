from setuptools import setup, find_packages

setup(
    name="pmpt-cli",
    version="0.1.2",
    description="CLI tool for AI-powered prompt enhancement",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.3.0",
        "prompt-toolkit>=3.0.36", 
        "rich>=13.0.0",
        "questionary>=2.0.0",
        "aiohttp>=3.8.0",
        "packaging>=21.0",
        "click>=8.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pmpt=main:main",
        ],
    },
    author="hawier-dev",
    author_email="",
    url="https://github.com/hawier-dev/pmpt-cli",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
