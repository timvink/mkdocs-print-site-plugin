# mkdocs-print-page-plugin

[MkDocs](https://www.mkdocs.org/) plugin that adds a page to your site combining all pages, allowing your site visitors to *File > Print > Save as PDF* the entire site.

## Installation

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

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.
