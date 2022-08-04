import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="acdpnet",
    version="2.1.3",
    author="Aiden Hopkins",
    author_email="acdphc@qq.com",
    description="A TCP Services Frame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A03HCY/Network-Core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)