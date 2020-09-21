import jinja2

from mkdocs_print_site_plugin.urls import fix_internal_links


class Renderer(object):
    def __init__(
        self,
        plugin_config,
        mkdocs_config={},
        cover_page_template_path="",
        insert_explain_block=True,
        print_page=None,
    ):
        """
        Args:
            insert_toc (bool): Insert a table of contents?
            insert_explain_block (bool): Insert a block explaining that this is a print page
        """

        self.plugin_config = plugin_config
        self.mkdocs_config = mkdocs_config
        self.cover_page_template_path = cover_page_template_path
        self.insert_explain_block = insert_explain_block
        self.print_page = print_page

        self.pages = []

    def write_combined(self):

        enabled_classes = []

        # Enable options via CSS
        if self.plugin_config.get("add_full_urls"):
            enabled_classes.append("print-site-add-full-url")

        if self.plugin_config.get("enumerate_headings"):
            enabled_classes.append("print-site-enumerate-headings")

        if self.plugin_config.get("enumerate_figures"):
            enabled_classes.append("print-site-enumerate-figures")

        # Wrap entire print page in a div
        # Enables CSS to be applied only to print-site-page
        html = '<div id="print-site-page" class="%s">' % " ".join(enabled_classes)

        # Enable options via HTML injection
        if self.plugin_config.get("add_cover_page"):
            html += self._cover_page()

        if self.insert_explain_block:
            html += self._explain_block()

        if self.plugin_config.get("add_table_of_contents"):
            html += self._toc()

        # Update internal anchor links
        page_htmls = [fix_internal_links(p.html, p.url) for p in self.pages]
        html += "".join(page_htmls)

        html += "</div>"

        return html

    def _cover_page(self):

        env = jinja2.Environment()
        env.globals = {"config": self.mkdocs_config, "page": self.print_page}

        with open(
            self.cover_page_template_path, "r", encoding="utf-8-sig", errors="strict"
        ) as f:
            cover_page_tpl = f.read()

        cover_page_html = env.from_string(cover_page_tpl).render()

        return (
            """
        <section id="print-site-cover-page">
            %s
        </section>
        """
            % cover_page_html
        )

    @staticmethod
    def _explain_block():
        return """
        <div id="print-site-banner">
            <p>
                <em>This box will disappear when printing</em>
                <span style="float: right"><a href="https://timvink.github.io/mkdocs-print-site-plugin/">mkdocs-print-site-plugin</a></span>
            </p>
            <p>This page combines all site pages and applies print and PDF friendly styling. Print or export to PDF using <b>File > Print > Save as PDF</b></p>
        </div>
        """

    @staticmethod
    def _toc():
        return """
        <section class="print-page">
            <div id="print-page-toc"></div>
        </section>
        """
