from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-print-site-plugin",
    version="0.0.1",
    description="Add print site page",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mkdocs plugin",
    url="https://github.com/timvink/mkdocs-print-site-plugin",
    author="Tim Vink",
    author_email="vinktim@gmail.com",
    include_package_data=True,
    license="MIT",
    python_requires=">=3.5",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["mkdocs>=1.0"],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "print-site = mkdocs_print_site_plugin.plugin:PrintSitePlugin"
        ]
    },
)
