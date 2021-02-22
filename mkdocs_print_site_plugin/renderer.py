import jinja2
import logging

from mkdocs_print_site_plugin.urls import fix_internal_links
from mkdocs_print_site_plugin.exclude import exclude

logger = logging.getLogger("mkdocs.plugins")


class Renderer(object):
    """
    Renders the print site page.
    """

    def __init__(
        self,
        plugin_config,
        mkdocs_config={},
        cover_page_template_path="",
        banner_template_path="",
        insert_print_site_banner=True,
        print_page=None,
    ):
        """
        Inits the class.
        """
        self.plugin_config = plugin_config
        self.mkdocs_config = mkdocs_config
        self.cover_page_template_path = cover_page_template_path
        self.banner_template_path = banner_template_path
        self.insert_print_site_banner = insert_print_site_banner
        self.print_page = print_page

        self.items = []

    def write_combined(self):
        """
        Generates the HTML of the page that combines all page into one.
        """
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

        if self.insert_print_site_banner:
            html += self._print_site_banner()

        if self.plugin_config.get("add_table_of_contents"):
            html += self._toc()

        def get_html_from_items(items: list, dir_urls: bool, excluded_pages: list, section_depth: int = 0) -> str:
            """
            Get all the HTML from the pages.
            """
            item_html = ""

            for item in items:
                if item.is_page:
                    # Do not include page in print page if excluded
                    if exclude(item.file.src_path, excluded_pages):
                        logging.debug("Excluding page " + item.file.src_path)
                        continue

                    # If you specify the same page twice in your navigation, it is only rendered once
                    # so we need to check if the html attribute exists
                    if hasattr(item, "html"):
                        if item.html == "":
                            logger.warning("[mkdocs-print-site] %s is empty and will be ignored" % item.file.src_path)
                            continue
                        # Update internal anchor links, image urls, etc
                        item_html += fix_internal_links(item.html, item.url, directory_urls=dir_urls)

                if item.is_section:
                    item_html += "<h%s class='nav-section-title'>%s</h1>" % (
                        min(6, section_depth + 1),
                        item.title,
                    )
                    item_html += get_html_from_items(item.children, dir_urls, excluded_pages, section_depth + 1)
                    # We also need to indicate the end of section page
                    # We do that using a h1 with a specific class
                    # In CSS we display:none, in JS we can use it for formatting the table of contents.
                    item_html += "<h1 class='nav-section-title-end'>Ended: %s</h1>" % item.title
            return item_html

        html += get_html_from_items(
            self.items,
            dir_urls=self.mkdocs_config.get("use_directory_urls"),
            excluded_pages=self.plugin_config.get("exclude", []),
        )

        html += "</div>"

        return html

    def _cover_page(self):
        """
        Inserts the cover page.
        """
        env = jinja2.Environment()
        env.globals = {"config": self.mkdocs_config, "page": self.print_page}

        with open(self.cover_page_template_path, "r", encoding="utf-8-sig", errors="strict") as f:
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

    def _print_site_banner(self):
        """
        Inserts the print site banner.
        """
        env = jinja2.Environment()
        env.globals = {"config": self.mkdocs_config, "page": self.print_page}

        with open(self.banner_template_path, "r", encoding="utf-8-sig", errors="strict") as f:
            banner_tpl = f.read()

        banner_html = env.from_string(banner_tpl).render()

        return f"""
        <div id="print-site-banner">
            {banner_html}
        </div>
        """

    def _toc(self):
        """
        Inserts the table of contents.
        """
        return f"""
        <section class="print-page">
            <div id="print-page-toc" data-toc-depth="{self.plugin_config.get("toc_depth")}">
                <nav role='navigation' class='print-page-toc-nav'>
                <h1 class='print-page-toc-title'>{self.plugin_config.get("toc_title")}</h1>
                </nav>
            </div>
        </section>
        """
