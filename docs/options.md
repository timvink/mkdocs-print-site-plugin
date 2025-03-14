# Options

You can customize `mkdocs-print-site-plugin` in your `mkdocs.yml` with the following settings:

```yaml
plugins:
  - print-site:
      add_to_navigation: false
      print_page_title: 'Print Site'
      print_page_basename: 'print_page'
      add_print_site_banner: false
      # Table of contents
      add_table_of_contents: true
      toc_title: 'Table of Contents'
      toc_depth: 6
      # Content-related
      add_full_urls: false
      enumerate_headings: true
      enumerate_figures: true
      add_cover_page: true
      cover_page_template: ""
      path_to_pdf: ""
      include_css: true
      enabled: true
      exclude:
```

`add_to_navigation`
:   Default is `false`. Adds a link 'Print Site' to your site navigation. You can also set to `false` and explicitly include the link in your navigation (`/print_page` or `/print_page.html`).

`print_page_title`
:   Default is `'Print Site'`. When `add_to_navigation` is set to `true` this setting controls the name of the print page in the navigation of the site. This setting is ignored when `add_to_navigation` is set to `false`.

`print_page_basename`
:   Default is `'print_page'`. Can be used to cutomized the path to the print page in the URL.

`add_table_of_contents`
:   Default is `true`. Adds a table of contents section at the beginning of the print page (in print version, the HTML version has a different sidebar ToC).

`toc_title`
:   Default is `'Table of Contents'`. When `add_table_of_contents` is set to `true` this setting controls the name of the table of contents of the print version of the print page. This setting is ignored when `add_table_of_contents` is set to `false`.

`toc_depth`
:   Default is `3`. When `add_table_of_contents` is set to `true` this setting controls the depth of the table of contents in the print version of the print page. This setting is ignored when `add_table_of_contents` is set to `false`.

`add_full_urls`
:   Default is `false`. When printing a page, you cannot see the target of a link. This option adds the target url in parenthesis behind a link.

    For example "[google.com](https://www.google.com)" will be replaced by "[google.com](https://www.google.com) (https://www.google.com)"

`enumerate_headings`
:   Default `true`. This will add numbering (enumeration) to all headings and sections, as well as the table of contents. Note this will only enumerate the print site page; if you want to enumerate the entire site, you can use [mkdocs-enumerate-headings-plugin](https://github.com/timvink/mkdocs-enumerate-headings-plugin).

    Example "1.2 A chapter subsection".

`enumerate_headings_depth`
:   Default `6`. If `enumerate_headings`, the depth until which headings and sections are enumerated.

`enumerate_figures`
:   Default `true`. This will add numbering to all figure captions (for example "Figure 1: <caption>"). Works especially well with [mkdocs-img2fig-plugin](https://github.com/stuebersystems/mkdocs-img2fig-plugin).

`add_cover_page`
:   Default `false`. When enabled, a cover page is added to the print page, displaying the `site_title` and other information from the `mkdocs.yml` file. See also [Customizing the cover page](how-to/cover_page.md)

`cover_page_template`
:   Default `""`. The path to a custom cover page template to use. See [Customizing the Cover Page](how-to/cover_page.md) for more info.

`add_print_site_banner`
:   Default `false`. When enabled, a banner is added to the top of the HTML print page, explaining to users the current page contains all site pages. See [Customizing the print site banner](how-to/banner.md) for more info.

`print_site_banner_template`
:   Default `""`. The path to a custom print site banner template to use. See [Customizing the print site banner](how-to/banner.md) for more info.

`path_to_pdf`
: Default is empty. Option to make it easier to add a link to the PDF version of the site on each page. See [Adding a PDF button](how-to/pdf_button.md) for more info.

`include_css`
: Default is `true`. When disabled the [print-site stylesheets](https://github.com/timvink/mkdocs-print-site-plugin/tree/master/mkdocs_print_site_plugin/css) are not included. This makes it easy to overwrite the CSS with your own stylesheets, using the [extra_css](https://www.mkdocs.org/user-guide/configuration/#extra_css) option in your `mkdocs.yml` file.

`enabled`
: Default is `true`. Enables you to deactivate this plugin. A possible use case is local development where you might want faster build times. It's recommended to use this option with an environment variable together with a default fallback (introduced in `mkdocs` v1.2.1, see [docs](https://www.mkdocs.org/user-guide/configuration/#environment-variables)). Example:

    ```yaml
    # mkdocs.yml
    plugins:
        - print-site:
            enabled: !ENV [ENABLED_PRINT_SITE, True]
    ```

    Which enables you do disable the plugin locally using:

    ```bash
    export ENABLED_PRINT_SITE=false
    mkdocs serve
    ```

`exclude`
: Default is empty. Allows to specify a list of page source paths that should not be included in the print page. Supports [glob](https://docs.python.org/3/library/glob.html)-like syntax such as `folder/` or `folder/*`. See [Do Not Print](how-to/do_not_print.md#ignoring-an-entire-page) for more info on excluding pages.