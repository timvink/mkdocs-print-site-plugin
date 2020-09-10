from mkdocs_print_site_plugin.urls import fix_internal_links


class Renderer(object):
    def __init__(self, theme_name, insert_toc=True, insert_explain_block=True):
        """
        Args:
            theme_name (str): Used to insert the corresponding CSS into the print page
            insert_toc (bool): Insert a table of contents?
            insert_explain_block (bool): Insert a block explaining that this is a print page
        """

        self.theme_name = theme_name
        self.insert_toc = insert_toc
        self.insert_explain_block = insert_explain_block

        self.pages = []

    def write_combined(self):

        # def fix_link(page, url):
        #     page_key = get_page_key(page.url)
        #     return "#" + page_key + "-" + url[1:]

        # for page in self.pages:
        #     print(f"Page {page.title}")
        #     for item in page.toc.items:
        #         print(f"'{item.title}' with link '{item.url}', new link {fix_link(page, item.url)}")
        #         for child in item.children:
        #             print(f"\tChild '{child.title}' with link '{child.url}', new link {fix_link(page, child.url)}")

        html = ""

        if self.insert_explain_block:
            html += self._explain_block()

        if self.insert_toc:
            html += self._toc()

        page_htmls = [fix_internal_links(p.html, p.url) for p in self.pages]
        html += "".join(page_htmls)
        return html

    @staticmethod
    def _explain_block():
        return """
        <div id="print-site-banner">
            <p>
                <em>This box will disappear when printing</em>
                <span style="float: right"><a href="https://timvink.github.io/mkdocs-print-site-plugin/">mkdocs-print-site-plugin</a></span>
            </p>
            <p>This page combines all pages in the site. This makes it easy to print or export to PDF (<b>File > Print > Save as PDF</b>)</p>
        </div>
        """

    @staticmethod
    def _toc():
        return """
        <section class="print-page">
            <div id="print-page-toc"></div>
        </section>
        """

    def insert_js_css_statements(self, html):
        """
        Inserts CSS and JS links into a HTML page
        """
        js = ""
        css = (
            """
        <link href="/css/print_site.css" rel="stylesheet">
        <link href="/css/print-site-%s.css" rel="stylesheet">
        """
            % self.theme_name
        )

        if self.insert_toc:
            js += """
            <script type="text/javascript" src="/js/print-site-toc.js"></script>
            """

        if self.theme_name == "material":
            js += """
            <script type="text/javascript" src="/js/print-site-material.js"></script>
            """

        html = html.replace("</head>", css + "</head>")
        html = html.replace("</body>", js + "</body>")
        return html
