import setuptools

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vlight",
    version="1.2.1",
    author="Amirreza salimi",
    author_email="amirrezasalimi0@gmail.com",
    description="a simple package for validation data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amirrezasalimi/vlight",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
