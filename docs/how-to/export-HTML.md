# Export to HTML

After enabling the `print-site` plugin in your `mkdocs.yml`, you will have your entire site combined into a single page. That allows you to create a standalone HTML page: a single self-contained file that has all images, styling and scripts embedded. This means you could send a site as an email attachment, a use case common within companies where deploying static sites might be more involved.

In order to create a self-contained, standalone HTML file from the print page, we will need to embed images, CSS and javascript using [data URLs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs). We can do this quite easily using the [htmlark](https://github.com/BitLooter/htmlark) python package:


```shell
pip install http html5lib requests
pip install htmlark
```

To create the export:

```shell
mkdocs build

cd site/

# when mkdocs.yml has use_directory_urls: true (the default)
htmlark print_page/index.html -o standalone.html

# when mkdocs.yml has use_directory_urls: false
htmlark print_page.html -o standalone.html
```
