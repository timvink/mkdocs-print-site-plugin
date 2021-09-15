# Customize the cover page

By default the `add_cover_page` option is set to `true`, which will add a cover page to the print page. You might want to customize it more to your liking.

You can do that by specifying the path to a custom cover page template in the `mkdocs.yml` file. This file should be a standard [jinja2 template](https://jinja.palletsprojects.com/en/2.11.x/templates/) where you can combine HTML and jinja2 variables. The information specified in `mkdocs.yml` will already by available as jinja2 variables (see [mkdocs project information](https://www.mkdocs.org/user-guide/configuration/#project-information)).

_Example_:

=== "mkdocs.yml"

    ```yaml
    plugins:
        - print-site:
            add_cover_page: true
            cover_page_template: "docs/assets/templates/custom_cover_page.tpl"
    ```

=== "docs/assets/templates/custom_cover_page.tpl"

    ```jinja
    {% if config.site_name %}
        <h1>{{ config.site_name }}</h1>
    {% endif %}
    <h2>This is my custom print cover page</h2>
    ```

To get you started have a look at the default [cover_page.tpl](https://github.com/timvink/mkdocs-print-site-plugin/tree/master/mkdocs_print_site_plugin/templates/cover_page.tpl).

## Adding images

When adding images to your custom cover page template, make sure to define the image source as the hosted image path. The url for the image stored in `docs/assets/img/example.png` would be `/assets/img/example.png`.

_Example_:

=== "docs/assets/templates/custom_cover_page.tpl"

    ```jinja
    {% if config.site_name %}
        <h1>{{ config.site_name }}</h1>
    {% endif %}
    <img src="/assets/img/example.png" />
    ```

For a full working example have a look at this [custom cover page with an image](https://github.com/timvink/mkdocs-print-site-plugin/blob/master/tests/fixtures/projects/with_markdown_ext/other_cover_page.tpl).

## Adding configurable content

You might want to add some content to your cover page that's not yet specified in your `mkdocs.yml` file. Of course you could just hard-code it in your custom template file, but you could also make use of MkDocs's [extra context](https://www.mkdocs.org/user-guide/custom-themes/#extra-context) feature, allowing you to use custom variables from your config file with `{{ config.extra.<your variable> }}`.

_Example_:

=== "mkdocs.yml"

    ```yaml
    plugins:
        - print-site:
            add_cover_page: true
            cover_page_template: "docs/assets/templates/custom_cover_page.tpl"
    
    extra:
        abstract: This is a report about a topic
    ```

=== "docs/assets/templates/custom_cover_page.tpl"

    ```jinja
    {% if config.site_name %}
        <h1>{{ config.site_name }}</h1>
    {% endif %}
    <p>{{ config.extra.abstract }}</p>
    ```

## Change the styling

You'll likely also want to change the styling of the cover page to your liking. You can add your own CSS file using the [extra_css](https://www.mkdocs.org/user-guide/configuration/#extra_css) option from MkDocs. `mkdocs-print-site-plugin` wraps the cover page in a `<section id="print-site-cover-page">`. You should use this in your CSS to ensure not affecting other pages.

_Example_:

=== "mkdocs.yml"

    ```yaml
    plugins:
        - print-site:
            add_cover_page: true

    extra_css:
        - docs/assets/css/my_cover_page.css
    ```

=== "docs/assets/css/my_cover_page.css"

    ```css
    #print-site-cover-page h1 {
        color: blue;
    }
    ```
