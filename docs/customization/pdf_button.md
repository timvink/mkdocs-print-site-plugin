# Adding a PDF button

You might want to make downloading a PDF even easier for your users. You could include a 'PDF' button on every page (like the one in the right corner of this page 👆)

MkDocs supports [theme extension](https://www.mkdocs.org/user-guide/styling-your-docs/#using-the-theme-custom_dir), an easy way to override parts of a theme.
You can use `page.url_to_print_page` to get the link to the site print page.

!!! info
    While it might be easier for your users, using this option means you need to manually create the PDF everytime you make a change to your website.

    If you use this option and you are using version control like git, you might want to also [gitignore](https://git-scm.com/docs/gitignore) the PDF file.

## Adding a PDF button to mkdocs-material theme

In `mkdocs-material` theme (see [customization](https://squidfunk.github.io/mkdocs-material/customization/#overriding-template-blocks)), you can create a file for overrides and point to it your `mkdocs.yml`. You might also want to disable adding the print page to the navigation when you already have a button with the link.

_Example_:

=== "mkdocs.yml"

    ```yaml
    theme:
    name: material
    custom_dir: docs/overrides

    plugin:
        - print-site:
            - path_to_pdf: "assets/the_name_of_your_file.pdf"
            - add_to_navigation: false
    ```

=== "docs/overrides/main.html"

    ```jinja
    {% extends "base.html" %}

    {% if page.url_to_pdf %}
        <a href="{{ page.url_to_pdf }}" title="Site PDF" class="md-content__button md-icon">
            {% include ".icons/material/pdf-box.svg" %}
        </a>
    {% endif %}

    {{ super() }}
    {% endblock content %}
    ```


## Adding a print button to mkdocs theme

You can also [customize](https://www.mkdocs.org/user-guide/custom-themes/#creating-a-custom-theme) the base mkdocs theme, by creating a file for overrides and pointing to it your `mkdocs.yml`. You might also want to disable adding the print page to the navigation when you already have a button with the link.

_Example_:

=== "mkdocs.yml"

    ```yaml
    theme:
        name: mkdocs
        custom_dir: docs/overrides

    plugin:
        - print-site:
            - path_to_pdf: "assets/the_name_of_your_file.pdf"
            - add_to_navigation: false
    ```

=== "docs/overrides/main.html"

    ```jinja
    {% extends "base.html" %}

    {% block repo %}
        {% if page.url_to_pdf %}
            <li class="nav-item">
                <a href="{{ page.url_to_pdf }}" title="Site PDF" class="nav-link">
                    <i class="fas fa-file-pdf"></i> PDF
                </a>
            </li>
        {% endif %}

    {{ super() }}
    {% endblock repo %}
    ```
