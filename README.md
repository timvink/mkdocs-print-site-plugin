# mkdocs-print-site-plugin

> ⚠️ **This plugin is under development and the first version has not yet been released. Expected end of August :)**

[MkDocs](https://www.mkdocs.org/) plugin that adds a page to your site combining all pages, allowing your site visitors to *File > Print > Save as PDF* the entire site.

## Features :star2:

- Allow visitors to create PDFs from MkDocs sites themselves
- Support for pagination
- Support for generic and [mkdocs-material](https://github.com/squidfunk/mkdocs-material) themes, but works on all themes
- Lightweight, no dependencies

Currently, there is no support for PDF bookmarks. Have a look at alternatives like [mkdocs-pdf-export-plugin]() and [mkdocs-pdf-with-js-plugin](https://github.com/smaxtec/mkdocs-pdf-with-js-plugin).

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

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

## Documentation

Available at [timvink.github.io/mkdocs-print-page-plugin](https://timvink.github.io/mkdocs-print-page-plugin/).

## TODO

- Perhaps prevent the write file, by having the .md file be part of the package? Or put it in a tmp folder? See # https://github.com/greenape/mknotebooks/blob/master/mknotebooks/plugin.py#L126
- Add a demo website
- Document known issues 
    - (PDF bookmarks
    -  [instant loading](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/#instant-loading) feature with mkdocs material) 
- tabbed content, only first tab prints.. (try to fix)
- Try to get PDF bookmarks working. Standards: https://www.w3.org/TR/2014/WD-css-gcpm-3-20140513/#bookmarks , lessons https://print-css.rocks/lessons
- Add print button to every page? See approach described at https://github.com/danielfrg/mkdocs-jupyter
- Ensure order of pages is consistent with navigation order, by making sure the plugin has been added last in the list.
- ensure this plugin is defined last (to allow other plugins to make any modifications first). Return a warning if this is not the case.
- Add option to change the print page title.
- Add option to insert a Table of contents page. Here is how to create the leader dots and page numbers using CSS https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/
- Add option to insert a frontcover page http://blog.michaelperrin.fr/2019/11/04/printing-the-web-part-2-html-and-css-for-printing-books/
- Display current chapter title in the footer http://blog.michaelperrin.fr/2019/11/04/printing-the-web-part-2-html-and-css-for-printing-books/ 
- check if appending print page does not break nested navigations (perhaps unit test?)
- check tables with lots of columns, deal with overflow
- Option to add print url after links? https://css-tricks.com/snippets/css/print-url-after-links/
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