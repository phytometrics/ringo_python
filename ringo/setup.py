from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ringo",
    version="0.1.0",
    author="RINGO Team",
    author_email="example@example.com",
    description="シリアル通信を簡単に扱うためのラッパーパッケージ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RINGO_python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyserial>=3.4",
    ],
)