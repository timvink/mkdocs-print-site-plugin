from mkdocs_print_site_plugin.urls import fix_internal_links


class Renderer(object):
    def __init__(self):
        self.pages = []
        self.insert_explain_block = True

    def write_combined(self):
        html = ""

        if self.insert_explain_block:
            html += self._explain_block()

        page_htmls = [fix_internal_links(p.html, p.url) for p in self.pages]
        html += "".join(page_htmls)
        return html

    def _explain_block(self):
        return """
        <div id="print-site-banner">
            <h3>Print Site Page</h3>
            <p>This page combines all pages in the site. This makes it easy to print or export to PDF (<b>File > Print > Save as PDF</b>)</p>
            <p><em>This message will disappear when printing this page</em></p>
        </div>
        """
