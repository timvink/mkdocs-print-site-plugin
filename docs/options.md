# Options

You can customize `mkdocs-print-site-plugin` in your `mkdocs.yml` with the following settings:

```yaml
plugins:
  - print-site:
      add_to_navigation: true
      print_page_title: 'Print Site'
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
      enabled: true
      exclude:
```

`add_to_navigation`
:   Default is `true`. Adds a link 'Print Site' to your site navigation. You can also set to `false` and explicitly include the link in your navigation (`/print_page` or `/print_page.html`).

`print_page_title`
:   Default is `'Print Site'`. When `add_to_navigation` is set to `true` this setting controls the name of the print page in the navigation of the site. This setting is ignored when `add_to_navigation` is set to `false`.

`add_table_of_contents`
:   Default is `true`. Adds a table of contents section at the beginning of the print page.

`toc_title`
:   Default is `'Table of Contents'`. When `add_table_of_contents` is set to `true` this setting controls the name of the table of contents. This setting is ignored when `add_table_of_contents` is set to `false`.

`toc_depth`
:   Default is `6`. When `add_table_of_contents` is set to `true` this setting controls the depth of the table of contents. This setting is ignored when `add_table_of_contents` is set to `false`.

`add_full_urls`
:   Default is `false`. When printing a page, you cannot see the target of a link. This option adds the target url in parenthesis behind a link.

    For example "[google.com](https://www.google.com)" will be replaced by "[google.com](https://www.google.com) (https://www.google.com)"

`enumerate_headings`
:   Default `false`. This will add numbering (enumeration) to all headings as well as the table of contents. Note this will only enumerate the print site page; if you want to enumerate the entire site, you can use [mkdocs-enumerate-headings-plugin](https://github.com/timvink/mkdocs-enumerate-headings-plugin).

    Example "1.2 A chapter subsection".

`enumerate_figures`
:   Default `false`. This will add numbering to all figure captions (for example "Figure 1: <caption>"). Works especially well with [mkdocs-img2fig-plugin](https://github.com/stuebersystems/mkdocs-img2fig-plugin).

`add_cover_page`
:   Default `false`. When enabled, a cover page is added to the print page, displaying the `site_title` and other information from the `mkdocs.yml` file. See also [Customizing the cover page](customization/cover_page.md)

`cover_page_template`
:   Default `""`. The path to a custom cover page template to use. See [Customizing the Cover Page](customization/cover_page.md) for more info.

`add_print_site_banner`
:   Default `true`. When enabled, a banner is added to the top of the print page, explaining to users the current page contains all site pages.

`print_site_banner_template`
:   Default `""`. The path to a custom print site banner template to use. See [Customizing the print site banner](customization/banner.md) for more info.

`path_to_pdf`
: Default is empty. Option to make it easier to add a link to the PDF version of the site on each page. See [Adding a PDF button](customization/pdf_button.md) for more info.

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
: Default is empty. Allows to specify a list of page source paths that should not be included in the print page. See [Do Not Print](customization/do_not_print.md#ignoring-an-entire-page) for more info.