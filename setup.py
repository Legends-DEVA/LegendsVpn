from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legendsvpn",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python-based VPN management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/legendsvpn",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: Proxy Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "beautifulsoup4>=4.12.0",
        "urllib3>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "legendsvpn=legendsvpn.cli:main",
        ],
    },
)
