# Options

You can customize the plugin by setting options in `mkdocs.yml`. This site uses the following settings:

```yaml
plugins:
  - print-site:
      add_to_navigation: true
      print_page_title: 'Print Site'
      add_table_of_contents: true
      add_full_urls: false
      enumerate_headings: true
      enumerate_figures: true
      add_cover_page: true
      cover_page_template: ""
```

## `add_to_navigation`

Default is `true`. Adds a link 'Print Site' to your site navigation.

## `print_page_title`

Default is `'Print Site'`. When `add_to_navigation` is set to `true` this setting controls the name of the print page in the navigation of the site. This setting is ignored when `add_to_navigation` is set to `false`.

## `add_table_of_contents`

Default is `true`. Adds a table of contents section at the beginning of the print page.

## `add_full_urls`

Default is `false`. When printing a page, you cannot see the target of a link. This option adds the target url in parenthesis behind a link. For example "[google.com](https://www.google.com)" will be replaced by "[google.com](https://www.google.com) (https://www.google.com)"

## `enumerate_headings`

Default `false`. This will add numbering (enumeration) to all headings as well as the table of contents. Example "1.2 A chapter subsection".

## `enumerate_figures`

Default `false`. This will add numbering to all figure captions (for example "Figure 1: <caption>"). Works especially well with [mkdocs-img2fig-plugin](https://github.com/stuebersystems/mkdocs-img2fig-plugin).

## `add_cover_page`

Default `true`. When enabled, a cover page is added to the print page, displaying the `site_title` and other information from the `mkdocs.yml` file. See also [Customizing the cover page](cover_page.md)

## `cover_page_template`

Default `""`. The path to a custom cover page template to use. See [Customizing the cover page](cover_page.md) for more info.