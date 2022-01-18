from setuptools import setup, find_packages

# Read README in UTF-8
with open("README.md", "r", encoding="UTF-8") as f:
    long_description = ""
    for line in f:
        long_description += line


setup(
    name="mkdocs-print-site-plugin",
    version="2.2.5",
    description="MkDocs plugin that combines all pages into one, allowing for easy export to PDF and standalone HTML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mkdocs plugin print pdf",
    url="https://github.com/timvink/mkdocs-print-site-plugin",
    author="Tim Vink",
    author_email="vinktim@gmail.com",
    include_package_data=True,
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Documentation",
        "Topic :: Text Processing",
    ],
    install_requires=["mkdocs-material>=7.3.0"],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "print-site = mkdocs_print_site_plugin.plugin:PrintSitePlugin"
        ]
    },
)
