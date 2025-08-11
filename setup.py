from setuptools import setup, find_packages

setup(
    name="pmpt-cli",
    version="0.1.5",
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
    py_modules=['pmpt_main'],
    entry_points={
        "console_scripts": [
            "pmpt=pmpt_main:main",
        ],
    },
    author="hawier-dev",
    author_email="mikolajbadyl0@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
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
