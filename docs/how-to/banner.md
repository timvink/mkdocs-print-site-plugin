# Customize the print site banner

When a user visits the print page, it might not be immediately obvious how to use it. You can set the `add_print_site_banner` option to `true` to add a banner to the top of the HTML print page that will be hidden when printing.

You might want to customize this banner, for example by translating it to your language. You can do that by specifying the path to a custom banner template in the `mkdocs.yml` file. This file should be a standard [jinja2 template](https://jinja.palletsprojects.com/en/2.11.x/templates/) where you can combine HTML and jinja2 variables. The information specified in `mkdocs.yml` will already by available as jinja2 variables (see [mkdocs project information](https://www.mkdocs.org/user-guide/configuration/#project-information)).

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
    <p>
        <em>This box will disappear when printing</em>
        <span style="float: right"><a href="https://timvink.github.io/mkdocs-print-site-plugin/">mkdocs-print-site-plugin</a></span>
    </p>
    <p>This page has combined all site pages into one. You can export to PDF using <b>File > Print > Save as PDF</b>.</p>
    <p>See also [export to PDF](https://timvink.github.io/mkdocs-print-site-plugin/how-to/export-PDF.html) and [export to standalone HTML](https://timvink.github.io/mkdocs-print-site-plugin/how-to/export-HTML.html).</p>
    ```

As an example, have a look at the default [print_site_banner.tpl](https://github.com/timvink/mkdocs-print-site-plugin/tree/master/mkdocs_print_site_plugin/templates/print_site_banner.tpl).

## Adding configurable content

You might want to add some content to your cover page that's not yet specified in your `mkdocs.yml` file.
Of course you could just hard-code it in your custom template file, but you could also make use of MkDocs's [extra context](https://www.mkdocs.org/user-guide/custom-themes/#extra-context) feature, allowing you to use custom variables from your config file with `{{ config.extra.<your variable> }}`.

_Example_:

=== "mkdocs.yml"

    ```yaml
    plugins:
        - print-site:
            add_print_site_banner: true
            print_site_banner_template: "docs/assets/templates/custom_banner.tpl"

    extra:
        banner_message: "Save this page using File > Print > Save as PDF"
    ```

=== "docs/assets/templates/custom_banner.tpl"

    ```jinja
    <p>
        <em>This box will disappear when printing</em>
        <span style="float: right"><a href="https://timvink.github.io/mkdocs-print-site-plugin/">mkdocs-print-site-plugin</a></span>
    </p>
    <p>{{ config.extra.banner_message }}</p>
    ```


