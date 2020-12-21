# Do not print

You might want to exclude certain parts of you website from the print site page. This can be useful when you don't want to include large images, tables, certain [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions) or appendixes to your site PDF.

## Ignoring certain elements in a page

`mkdocs-print-site-plugin` offers the CSS class `.print-site-plugin-ignore`, that will ignore certain elements.

The [Attribute Lists](https://python-markdown.github.io/extensions/attr_list/) extension, which is part of the standard Markdown library, allows to add HTML attributes and CSS classes to Markdown elements, and can be enabled via `mkdocs.yml`.

To apply the `.print-site-plugin-ignore` class to an element, you can add `{: .print-site-plugin-ignore }` to many markdown elements, as explained in the [attr_list docs](https://python-markdown.github.io/extensions/attr_list/). `attr_list` does not support all markdown elements (see [limitations](https://python-markdown.github.io/extensions/attr_list/#limitations)), but remember Markdown is a subset of HTML and anything which cannot be expressed in Markdown can always be expressed with raw HTML directly.

_Example_:

=== "mkdocs.yml"

    ```yaml
    plugins:
        - print-site

    markdown_extensions:
        - attr_list
    ```

=== "docs/example.md"

    ```md
    # Example page

    This paragraph is not part of the print site page.
    {: .print-site-plugin-ignore }

    ![ignored image](some/path/image.png){: .print-site-plugin-ignore }

    You can also use HTML to hide things from printing:
    <span class="print-site-plugin-ignore">hello</span>
    ```

As another example, this paragraph will not be printed. Go have a look at the [print site page](/print_page.html) and you'll find it missing.
{: .print-site-plugin-ignore }

## Ignoring admonitions

Adding a class to [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions) is not supported by `attr_list`. You can use the `.print-site-plugin-ignore` class directly on admonitions however:

```markdown
!!! info print-site-plugin-ignore

    As an example, this admonition will not be printed. Go have a look at the [print site page](/print_page.html) and you'll find it missing.
```

Which renders as:

!!! info print-site-plugin-ignore

    As an example, this admonition will not be printed. Go have a look at the [print site page](/print_page.html) and you'll find it missing.


## Ignoring an entire page

Not yet implemented. Upvote [mkdocs-print-site-plugin#34](https://github.com/timvink/mkdocs-print-site-plugin/issues/34) if you're interested.