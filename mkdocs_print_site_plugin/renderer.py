import re
import jinja2
import logging

from mkdocs.structure.toc import AnchorLink, TableOfContents

from mkdocs_print_site_plugin.urls import (
    fix_internal_links,
    get_page_key,
    to_snake_case,
)
from mkdocs_print_site_plugin.exclude import exclude

logger = logging.getLogger("mkdocs.plugins")


class Renderer(object):
    """
    Renders the print site page.
    """

    def __init__(
        self,
        plugin_config,
        mkdocs_config=None,
        cover_page_template_path="",
        banner_template_path="",
        print_page=None,
    ):
        """
        Inits the class.
        """
        self.plugin_config = plugin_config
        self.mkdocs_config = mkdocs_config or {}
        self.cover_page_template_path = cover_page_template_path
        self.banner_template_path = banner_template_path
        self.print_page = print_page

        self.items = []

    def _get_items(self):
        return [i for i in self.items if not i == self.print_page]

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

        if self.plugin_config.get("add_print_site_banner"):
            html += self._print_site_banner()

        if self.plugin_config.get("add_table_of_contents"):
            html += self._toc()

        def get_html_from_items(
            items: list, dir_urls: bool, excluded_pages: list, section_depth: int = 0
        ) -> str:
            """
            Get all the HTML from the pages.
            """
            items_html = ""

            for item in items:
                if item.is_page:
                    # Do not include page in print page if excluded
                    if exclude(item.file.src_path, excluded_pages):
                        logging.debug(f"Excluding page '{item.file.src_path}'")
                        continue

                    # If you specify the same page twice in your navigation, it is only rendered once
                    # so we need to check if the html attribute exists
                    if hasattr(item, "html"):
                        if item.html == "":
                            logger.warning(
                                f"[mkdocs-print-site] {item.file.src_path} is empty and will be ignored"
                            )
                            continue

                        item_html = item.html

                        # Add missing h1 tag if the first heading is not a h1
                        match = re.search(r"\<h[0-6]", item_html)
                        if match:
                            if not match.group() == "<h1":
                                item_html = f'<h1 id="{to_snake_case(item.title)}">{item.title}</h1>{item_html}'
                                logger.warning(
                                    f"[mkdocs-print-site] '{item.file.src_path}' file is missing a leading h1 tag. Added to the print-page with title '{item.title}'"
                                )

                        # Support mkdocs-material tags
                        # See https://squidfunk.github.io/mkdocs-material/plugins/tags
                        if "tags" in item.meta:
                            tags = item.meta["tags"]
                            tags_html = "<nav class='md-tags'>"
                            for tag in tags:
                                tags_html += f"<span class='md-tag'>{tag}</span>"
                            tags_html += "</nav>"
                            item_html = tags_html + item_html

                        # Update internal anchor links, image urls, etc
                        items_html += fix_internal_links(
                            item_html, item.url, directory_urls=dir_urls
                        )

                if item.is_section:
                    items_html += """
                        <h%s class='nav-section-title' id='section-%s'>
                            %s <a class='headerlink' href='#section-%s' title='Permanent link'>↵</a>
                        </h%s>
                        """ % (
                        min(6, section_depth + 1),
                        to_snake_case(item.title),
                        item.title,
                        to_snake_case(item.title),
                        min(6, section_depth + 1),
                    )
                    items_html += get_html_from_items(
                        item.children, dir_urls, excluded_pages, section_depth + 1
                    )
                    # We also need to indicate the end of section page
                    # We do that using a h1 with a specific class
                    # In CSS we display:none, in JS we can use it for formatting the table of contents.
                    items_html += (
                        "<h1 class='nav-section-title-end'>Ended: %s</h1>" % item.title
                    )
            return items_html

        html += get_html_from_items(
            self._get_items(),
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

    def _print_site_banner(self):
        """
        Inserts the print site banner.
        """
        env = jinja2.Environment()
        env.globals = {"config": self.mkdocs_config, "page": self.print_page}

        with open(
            self.banner_template_path, "r", encoding="utf-8-sig", errors="strict"
        ) as f:
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

    def get_toc_sidebar(self) -> TableOfContents:
        """
        Generate a MkDocs a navigation sidebar.

        We want to generate one for the print page also, so we can export HTML.

        In general, this follows the same hierarchy as pages. However, page section and chapter
        numbers are generated by HTML/CSS. Here, we duplicate the same logic.

        Reference: https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/toc.py
        """

        excluded_pages = self.plugin_config.get("exclude", [])

        toc = self._toc_sidebar_layer(
            self._get_items(),
            excluded_pages,
            page_numbers=[],
        )

        return TableOfContents(toc)

    def _toc_sidebar_layer(
        self,
        items: list,
        excluded_pages: list,
        page_numbers: list[int],
    ) -> list[AnchorLink]:
        """
        A single recursive layer of navigation sidebar generation.

        Returns the items generated.
        """

        toc = []

        # The level is simply the number of section numbers we have (e.g. an empty list is the start
        # of recursion, at level 0).
        level = len(page_numbers)

        # Each recursion starts with a new section.
        current_page = 0

        for item in items:
            if item.is_page and exclude(item.file.src_path, excluded_pages):
                logging.debug(
                    f"Excluding page '{item.file.src_path}' from sidebar output"
                )
                continue

            # Bump the page number -- we assign new numbers to both pages and sections.
            current_page += 1

            if item.is_page:
                page_key = get_page_key(item.url)
                # navigate to top of page if page is homepage
                if page_key == "index":
                    page_key = ""

                if self.plugin_config.get("enumerate_headings"):
                    chapter = chapter_number(page_numbers, current_page)
                    title = f"{chapter}. {item.title}"
                else:
                    title = item.title

                toc.append(AnchorLink(title=title, id=f"{page_key}", level=level))

            if item.is_section:
                if self.plugin_config.get("enumerate_headings"):
                    chapter = chapter_number(page_numbers, current_page)
                    title = f"{chapter}. {item.title}"
                else:
                    title = item.title

                section_link = AnchorLink(
                    title=title, id=f"section-{to_snake_case(item.title)}", level=level
                )

                subpages = [
                    p
                    for p in item.children
                    if p.is_page and not exclude(p.file.src_path, excluded_pages)
                ]
                if len(subpages) > 0:
                    toc.append(section_link)

                # Now recurse into the children.
                child_toc = self._toc_sidebar_layer(
                    item.children,
                    excluded_pages,
                    page_numbers + [current_page],
                )
                section_link.children.extend(child_toc)

        return toc


def chapter_number(page_numbers: list[int], current_page: int) -> str:
    return ".".join([str(n) for n in page_numbers + [current_page]])
