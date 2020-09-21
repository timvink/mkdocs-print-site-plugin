# Customize the cover page

When the `add_cover_page` option is set to true, `mkdocs-print-site-plugin` will generate a cover page when printing. This cover page is quite basic, and you might want to customize it.

You can do that by specifying a custom cover page template in the `mkdocs.yml` file:

```yaml
# mkdocs.yml
add_cover_page: true
cover_page_template: "path/to/custom_cover_page.tpl"
```

This is a standard [jinja2 template](https://jinja.palletsprojects.com/en/2.11.x/templates/) file where you can combine HTML and use the information specified in `mkdocs.yml` as jinja2 variables.
As an example, have a look at the default [cover_page.tpl](https://github.com/timvink/mkdocs-print-site-plugin/tree/master/mkdocs_print_site_plugin/templates/cover_page.tpl).

## Adding extra content

You might want to add some content to your cover page that's not yet specified in your `mkdocs.yml` file. Of course you could just hard-code it in your custom template file, but you could also make use of MkDocs's [extra context](https://www.mkdocs.org/user-guide/custom-themes/#extra-context) feature:

```yaml
# mkdocs.yml
extra:
    abstract: This is a report about a topic
```

You can then use `{{ config.extra.abstract }}` in your custom template file to insert your abstract.

## Change the styling

You'll likely also need to change the styling to your liking. You can add your own CSS file using the [extra_css](https://www.mkdocs.org/user-guide/configuration/#extra_css) option from MkDocs:

```yaml
# mkdocs.yml
extra_css:
    - path/to/my_cover_page.css
```

`mkdocs-print-site-plugin` wraps the cover page in a `<section>` with id `print-site-cover-page`. You should use this in you CSS to ensure not affecting other pages. For example:

```css
/* my_cover_page.css */
#print-site-cover-page h1 {
    color: blue;
}
```