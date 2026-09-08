[![Actions Status](https://github.com/timvink/mkdocs-print-site-plugin/workflows/pytest/badge.svg)](https://github.com/timvink/mkdocs-print-site-plugin/actions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-print-site-plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-print-site-plugin)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mkdocs-print-site-plugin)
[![codecov](https://codecov.io/gh/timvink/mkdocs-print-site-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/timvink/mkdocs-print-site-plugin)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mkdocs-print-site-plugin)
![PyPI - License](https://img.shields.io/pypi/l/mkdocs-print-site-plugin)

# mkdocs-print-site-plugin

[MkDocs](https://www.mkdocs.org/) plugin that adds a page to your site combining all pages, allowing your site visitors to *File > Print > Save as PDF* the entire site.

## Installation

Install the plugin using `pip3`:

```bash
pip3 install mkdocs-print-site-plugin
```

Next, add the following lines to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - print-site
```

> :warning: Make sure to put `print-site` to the **bottom** of the plugin list. This is because other plugins might alter your site (like the navigation), and you want these changes included in the print page.

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Supported themes

The plugin ships print stylesheets (margins, page breaks, hiding navigation) for the
[mkdocs-material](https://github.com/squidfunk/mkdocs-material),
[mkdocs-materialx](https://github.com/jaywhj/mkdocs-materialx),
[mkdocs](https://www.mkdocs.org/user-guide/choosing-your-theme/#mkdocs) and
[readthedocs](https://www.mkdocs.org/user-guide/choosing-your-theme/#readthedocs) themes.

Other themes will still get a print page, but you'll see a warning that print margins and
page breaks might be off. Feel free to
[open an issue](https://github.com/timvink/mkdocs-print-site-plugin/issues) to request support
for your theme, or write your own stylesheet using the [`include_css`](options.md) option.

## Usage

- Navigate to `/print_page/` or `print_page.html`
- Export to standalone HTML (see [export to HTML](how-to/export-HTML.md))
- Export to PDF using your browser using *File > Print > Save as PDF*  (see [export to PDF](how-to/export-PDF.md))
