[![Actions Status](https://github.com/timvink/mkdocs-print-site-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-print-site-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-print-site-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-print-site-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-print-site-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-print-site-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-print-site-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-print-site-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-print-site-plugin)

# mkdocs-print-site-plugin

> ⚠️ **This plugin is under development and the first version has not yet been released. Expected end of August :)**

[MkDocs](https://www.mkdocs.org/) plugin that adds a page to your site combining all pages, allowing your site visitors to *File > Print > Save as PDF* the entire site.

## Features :star2:

- Allow visitors to create PDFs from MkDocs sites themselves
- Support for pagination
- Support for generic and [mkdocs-material](https://github.com/squidfunk/mkdocs-material) themes, but works on all themes
- Lightweight, no dependencies

Currently, there is no support for PDF bookmarks (see [#1](https://github.com/timvink/mkdocs-print-site-plugin/issues/1) for details). Have a look at alternatives like [mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin) and [mkdocs-pdf-with-js-plugin](https://github.com/smaxtec/mkdocs-pdf-with-js-plugin).

## Setup

Install the plugin using `pip3`:

```bash
pip3 install mkdocs-print-site-plugin
```

Next, add the following lines to your `mkdocs.yml`:

```yml
plugins:
  - search
  - print-site
```

> ⚠️ Make sure to put `print-site` to the **bottom** of the plugin list. This is because other plugins might alter your site (like the navigation), and you want these changes included in the print page.

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Documentation

Available at [timvink.github.io/mkdocs-print-site-plugin](https://timvink.github.io/mkdocs-print-site-plugin/).

## TODO for 1st release

- Write some basic build unit tests
- Perhaps prevent the write file, by having the .md file be part of the package? Or put it in a tmp folder? See # https://github.com/greenape/mknotebooks/blob/master/mknotebooks/plugin.py#L126
- Return a warning to the user if the `print-site` plugin is not defined last (to allow other plugins to make any modifications first).
- check if appending print page does not break nested navigations (perhaps unit test?)
- check tables with lots of columns, deal with overflow
- support different anchor links, or at least throw warning if different than #
  https://www.mkdocs.org/user-guide/writing-your-docs/
    ```yml
    markdown_extensions:
        - toc:
            permalink: "#"
    ```
- ensure support of 'use_directory_urls' settings https://www.mkdocs.org/user-guide/configuration/#use_directory_urls
    ```python
    [p.url for p in self.pages]
    ['index.html', 'z.html', 'a.html']
    ```


## Contributing

Contributions are very welcome! Start by reading the [contribution guidelines](https://timvink.github.io/mkdocs-print-site-plugin/contributing.html).