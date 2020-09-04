from mkdocs_print_site_plugin.urls import fix_internal_links


class Renderer(object):
    def __init__(self, theme_name):
        """
        Args:
            theme_name (str): Used to insert the corresponding CSS into the print page
        """

        self.theme_name = theme_name

        self.pages = []
        self.insert_explain_block = True

    def write_combined(self):
        html = ""

        if self.insert_explain_block:
            html += self._explain_block()

        page_htmls = [fix_internal_links(p.html, p.url) for p in self.pages]
        html += "".join(page_htmls)
        return html

    @staticmethod
    def _explain_block():
        return """
        <div id="print-site-banner">
            <h3>Print Site Page</h3>
            <p>This page combines all pages in the site. This makes it easy to print or export to PDF (<b>File > Print > Save as PDF</b>)</p>
            <p><em>This message will disappear when printing this page</em></p>
        </div>
        """

    def insert_css_statements(self, html):
        """
        Inserts CSS links into a HTML page
        """
        css = (
            """
        <link href="/css/print_site.css" rel="stylesheet">
        <link href="/css/%s.css" rel="stylesheet">
        """
            % self.theme_name
        )

        return html.replace("</head>", css + "</head>")
