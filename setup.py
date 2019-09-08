import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Sagrave",
    version="0.0.1",
    author="Yves Huguenin",
    author_email="yves.huguenin@tricala.org",
    description="Programme pour traiter les données de RZ Win",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alcatrazproduction/sagrave",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
