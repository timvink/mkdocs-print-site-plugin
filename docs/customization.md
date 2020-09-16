# Customization

You might want to customize your site to include a 'print' button on every page (like the one in the right corner of this page 👆)

MkDocs supports [theme extension](https://www.mkdocs.org/user-guide/styling-your-docs/#using-the-theme-custom_dir), an easy way to override parts of a theme.
You can use `page.url_to_print_page` to get the link to the site print page.

## Adding a print button to mkdocs-material theme

In `mkdocs-material` theme (see [customization](https://squidfunk.github.io/mkdocs-material/customization/#overriding-template-blocks)), first create a directory for overrides and update your `mkdocs.yml`:

```yml
theme:
  name: material
  custom_dir: docs/overrides
```
 
You can create the file `docs/overrides/main.html` as follows:

```
{% extends "base.html" %}

{% block content %}
{% if page.url_to_print_page %}
    <a href="{{ page.url_to_print_page }}" title="Print Site" class="md-content__button md-icon">
        {% include ".icons/material/printer.svg" %}
    </a>
{% endif %}

{{ super() }}
{% endblock content %}
```

## Adding a print button to mkdocs theme

You can also [customize](https://www.mkdocs.org/user-guide/custom-themes/#creating-a-custom-theme) the base mkdocs theme, by first creating an `overrides` directory:

```yml
theme:
    name: mkdocs
    custom_dir: docs/overrides
```

And then adding a file `docs/overrides/main.html` with the following content:

```html
{% extends "base.html" %}

{% block repo %}
    {% if page.url_to_print_page %}
        <li class="nav-item">
            <a href="{{ page.url_to_print_page }}" title="Print Site" class="nav-link">
                <i class="fa fa-print"></i> Print
            </a>
        </li>
    {% endif %}

{{ super() }}
{% endblock repo %}
```
