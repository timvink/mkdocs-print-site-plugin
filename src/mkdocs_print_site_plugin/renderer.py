import logging
import re
from typing import List, Tuple

import jinja2
from mkdocs.structure.toc import AnchorLink, TableOfContents

from mkdocs_print_site_plugin.exclude import exclude
from mkdocs_print_site_plugin.urls import (
    fix_internal_links,
    get_page_key,
)
from mkdocs_print_site_plugin.utils import get_section_id

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

    def write_combined(self) -> Tuple[str, TableOfContents]:
        """
        Generates the HTML of the page that combines all page into one, while filling
        a table of contents.
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

        def get_html_and_anchor_links_from_items(
            items: list,
            dir_urls: bool,
            excluded_pages: list,
            level: int = 0,
            prefix: str = "",
            heading_styles: List[str] = [],
        ) -> Tuple[str, List[AnchorLink]]:
            """
            Get all the HTML and anchor links from the pages.
            """
            items_html = ""
            anchor_links = []

            for i, item in enumerate(items):
                my_prefix = f"{prefix}{i + 1}"
                item_id = None
                title = item.title
                if self.plugin_config.get("enumerate_headings"):
                    title = f"{my_prefix} {title}"

                if item.is_page:
                    # Do not include page in print page if excluded
                    if exclude(item.file.src_path, excluded_pages):
                        logging.debug(f"Excluding page '{item.file.src_path}'")
                        continue

                    item_id = get_page_key(item.url)
                    anchor_links.append(AnchorLink(title, item_id, level))
                    heading_styles.append(
                        f".print-site-enumerate-headings #{item_id} > h1:before {{ content: '{my_prefix} ' }}"
                    )

                    # If you specify the same page twice in your navigation, it is only rendered once
                    # so we need to check if the html attribute exists
                    if hasattr(item, "html"):
                        if item.html == "":
                            logger.warning(f"[mkdocs-print-site] {item.file.src_path} is empty and will be ignored")
                            continue

                        item_html = item.html

                        # Add missing h1 tag if the first heading is not a h1
                        match = re.search(r"\<h[0-6]", item_html)
                        if match:
                            if not match.group() == "<h1":
                                item_html = f'<h1 id="{item_id}">{item.title}</h1>{item_html}'
                                logger.warning(
                                    f"[mkdocs-print-site] '{item.file.src_path}' file is missing a leading h1 tag. Added to the print-page with title '{item.title}'"
                                )

                        heading_styles.append(self._set_inner_heading_styles(item_id, my_prefix, level))

                        # Support mkdocs-material tags
                        # See https://squidfunk.github.io/mkdocs-material/plugins/tags
                        if hasattr(item, "meta") and item.meta.get("tags"):
                            tags = item.meta["tags"]
                            tags_html = "<nav class='md-tags'>"
                            for tag in tags:
                                tags_html += f"<span class='md-tag'>{tag}</span>"
                            tags_html += "</nav>"
                            item_html = tags_html + item_html

                        # Update internal anchor links, image urls, etc
                        items_html += fix_internal_links(
                            item_html, item.url, directory_urls=dir_urls, heading_number=my_prefix
                        )

                if item.is_section:
                    item_id = get_section_id(my_prefix)
                    heading_styles.append(
                        f".print-site-enumerate-headings #{item_id} > h1:before {{ content: '{my_prefix} ' }}"
                    )
                    items_html += f"""
                    <section class='print-page md-section' id='{item_id}' heading-number='{my_prefix}'>
                        <h1>{item.title}<a class='headerlink' href='#{item_id}' title='Permanent link'></a>
                        </h1>
                    """
                    section_html, section_links = get_html_and_anchor_links_from_items(
                        item.children, dir_urls, excluded_pages, level + 1, my_prefix + ".", heading_styles
                    )
                    items_html += section_html
                    section_link = AnchorLink(title, item_id, level)
                    section_link.children = section_links
                    anchor_links.append(section_link)

                    items_html += "</section>"

            return items_html, anchor_links

        heading_styles: List[str] = []
        items_html, anchor_links = get_html_and_anchor_links_from_items(
            self._get_items(),
            dir_urls=self.mkdocs_config.get("use_directory_urls"),
            excluded_pages=self.plugin_config.get("exclude", []),
            heading_styles=heading_styles,
        )

        html += items_html
        html += "</div>"
        html += "<style>" + "\n".join(heading_styles) + "</style>"

        return html, TableOfContents(anchor_links)

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

    def _set_inner_heading_styles(self, id: str, prefix: str, level: int) -> str:
        """
        By "inner heading" we mean that even if the heading numbers are fully determined by
        the nav's hierarchy, if a page has number 3.2.1, we will add a further numbering
        to headings such as h2 and h3 inside the page, so that the first h2 that appears is
        3.2.1.1, the next one is 3.2.1.2, etc. In this case we will require that the number
        of items in this index be <= toc_depth, which is not the case in the ToC (as its depth
        is fully determined by the nav's depth).
        """
        result = ""
        toc_depth = self.plugin_config.get("toc_depth") or 1
        # Start from h2's
        h_level = 2
        counter_names = [f"counter-{id}-{i}" for i in range(h_level, toc_depth - level + 1)]
        while h_level <= toc_depth - level:
            counters_to_reset = " ".join([f"{x} " for x in counter_names[h_level - 1 :]])
            counter_reset = f" counter-reset: {counters_to_reset}; " if len(counters_to_reset) > 0 else ""
            counters_to_display = " '.' ".join([f"counter({x})" for x in counter_names[: h_level - 1]])
            result += f"""
                .print-site-enumerate-headings #{id} h{h_level}:before {{ content: '{prefix}.' {counters_to_display} ' ' }}
                .print-site-enumerate-headings #{id} h{h_level} {{ {counter_reset} counter-increment: counter-{id}-{h_level} }}
            """
            h_level += 1

        return result
