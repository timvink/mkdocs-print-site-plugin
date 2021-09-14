# Customize the print site banner

When the `add_print_site_banner` option is set to true, `mkdocs-print-site-plugin` will add a banner to the top of the print page. You might want to customize this banner, for example by translating it to your language.

You can do that by specifying the path to a custom banner template in the `mkdocs.yml` file. This file should be a standard [jinja2 template](https://jinja.palletsprojects.com/en/2.11.x/templates/) where you can combine HTML and special jinja2 variables, such as the information specified in `mkdocs.yml` (see [mkdocs project information](https://www.mkdocs.org/user-guide/configuration/#project-information)).

_Example_:

=== "mkdocs.yml"

    ```yaml
    plugins:
        - print-site:
            add_print_site_banner: true
            print_site_banner_template: "docs/assets/templates/custom_banner.tpl"
    ```

=== "docs/assets/templates/custom_banner.tpl"

    ```jinja
    
    ```

As an example, have a look at the default [print_site_banner.tpl](https://github.com/timvink/mkdocs-print-site-plugin/tree/master/mkdocs_print_site_plugin/templates/print_site_banner.tpl).
