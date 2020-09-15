# Options

You can customize the plugin by setting options in `mkdocs.yml`. This site uses the following settings:

```yml
plugins:
  - print-site:
      add_to_navigation: true
      print_page_title: 'Print Site'
      add_table_of_contents: true
      add_full_urls: false
      enumerate_headings: true
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

Default `false`. This will add numbering to all headings, which is useful for larger sites.