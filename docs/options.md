# Options

You can customize the plugin by setting options in `mkdocs.yml`. For example:

```yml
plugins:
  - print-site:
      add_to_navigation: true
      print_page_title: 'Print Site'
```

## `add_to_navigation`

Default is `true`. Adds a link 'Print Site' to your site navigation.

## `print_page_title`

Default is 'Print Site'. When `add_to_navigation` is set to `true` this setting controls the name of the print page in the navigation of the site. This setting is ignored when `add_to_navigation` is set to `false`.