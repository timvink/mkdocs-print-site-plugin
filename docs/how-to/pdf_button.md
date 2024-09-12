# Adding a PDF button

Having users create a PDF of your website requires them to navigate to the print page and *File > Print > Save as PDF* (see [export to PDF](export-PDF.md)). You can make downloading a PDF version of your website even easier for your users by including a 'PDF' button on every page (like the one in the right corner of this page 👆).

MkDocs supports [theme extension](https://www.mkdocs.org/user-guide/styling-your-docs/#using-the-theme-custom_dir), an easy way to override parts of a theme. That will allow you to add a button to the top of every page.

This plugin adds to the context a `page.url_to_print_page` which contains the relative link from a page to the print page. You can use `page.url_to_print_page` when customizing a theme:

!!! info "Exporting to PDF is a separate step"
    While it might be easier for your users, using this option means you need to re-create the PDF everytime you make a change to your website. See [how to export to PDF](pdf_button.md).

    If you use this option and you are using version control like git, you might want to also [gitignore](https://git-scm.com/docs/gitignore) the PDF file.

## Adding a PDF button to mkdocs-material theme

In the [mkdocs-material](https://squidfunk.github.io/mkdocs-material) theme you can create an override for `main.html` (see [customization](https://squidfunk.github.io/mkdocs-material/customization/#overriding-template-blocks)).

_Example_:

=== "mkdocs.yml"

    ```yaml
    theme:
    name: material
    custom_dir: docs/overrides

    plugins:
        - print-site:
            path_to_pdf: "assets/the_name_of_your_file.pdf"
    ```

=== "docs/overrides/main.html"

    ```jinja
    {% extends "base.html" %}

    {% block content %}

    {% if page.url_to_pdf %}
        <a href="{{ page.url_to_pdf }}" title="Site PDF" class="md-content__button md-icon">
            {% include ".icons/material/file-pdf-box.svg" %}
        </a>
    {% endif %}

    {{ super() }}
    {% endblock content %}
    ```


## Adding a print button to mkdocs theme

You can also [customize](https://www.mkdocs.org/user-guide/custom-themes/#creating-a-custom-theme) the base mkdocs theme, by overriding `main.html`.

_Example_:

=== "mkdocs.yml"

    ```yaml
    theme:
        name: mkdocs
        custom_dir: docs/overrides

    plugins:
        - print-site:
            path_to_pdf: "assets/the_name_of_your_file.pdf"
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
