from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os
import tempfile
import logging

from pathlib import Path

from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.utils import write_file

from mkdocs_print_site_plugin.renderer import Renderer


HERE = os.path.dirname(os.path.abspath(__file__))
CSS_DIR = os.path.join(HERE, "css")
JS_DIR = os.path.join(HERE, "js")


class PrintSitePlugin(BasePlugin):

    config_scheme = (
        ("add_to_navigation", config_options.Type(bool, default=True)),
        ("print_page_title", config_options.Type(str, default="Print Site")),
        ("add_table_of_contents", config_options.Type(bool, default=True)),
    )

    def on_config(self, config, **kwargs):

        # Because other plugins can alter the navigation
        # (and thus which pages should be in the print page)
        # it is important 'print-site' is defined last in the 'plugins'
        plugins = config.get("plugins")
        print_site_position = [*dict(plugins)].index("print-site")
        if print_site_position != len(plugins) - 1:
            logging.warning(
                "[mkdocs-print-site] 'print-site' should be defined as the *last* plugin, to ensure the print page has any changes other plugins make. Please update the 'plugins:' section in your mkdocs.yml"
            )

        # Create the (empty) print page file in temp directory
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, "print_page.md")
        f = open(tmp_path, "w")
        f.write("")
        f.close()
        assert os.path.exists(tmp_path)

        # Create MkDocs Page and File instances
        self.print_file = File(
            path="print_page.md",
            src_dir=tmp_dir,
            dest_dir=config["site_dir"],
            use_directory_urls=config.get("use_directory_urls"),
        )
        self.print_page = Page(
            title=self.config.get("print_page_title"),
            file=self.print_file,
            config=config,
        )
        self.print_page.edit_url = None

        # Warn if we don't have CSS styles corresponding to current theme
        theme_name = config.get("theme").name
        theme_css_files = [Path(f).stem for f in os.listdir(CSS_DIR)]
        if theme_name not in theme_css_files:
            logging.warning(
                "[mkdocs-print-site] Theme %s not yet supported, which means print margins and page breaks might be off."
                % theme_name
            )

        # Save instance of the print page renderer
        self.renderer = Renderer(
            theme_name=theme_name,
            insert_toc=self.config.get("add_table_of_contents"),
            insert_explain_block=True,
        )

        return config

    def on_files(self, files, config, **kwargs):

        # Add all plugin JS and CSS files to files directory
        # Note we only include the relevant css and js files per theme into the print page file
        # in renderer.py
        css_dest_dir = os.path.join(config["site_dir"], "css")
        for file in os.listdir(CSS_DIR):
            files.append(
                File(
                    path=file,
                    src_dir=CSS_DIR,
                    dest_dir=css_dest_dir,
                    use_directory_urls=False,
                )
            )

        js_dest_dir = os.path.join(config["site_dir"], "js")
        for file in os.listdir(JS_DIR):
            files.append(
                File(
                    path=file,
                    src_dir=JS_DIR,
                    dest_dir=js_dest_dir,
                    use_directory_urls=False,
                )
            )

        return files

    def on_nav(self, nav, config, files, **kwargs):

        # Save the (order of) pages in the navigation
        self.renderer.pages = nav.pages.copy()  # nav_pages

        # Optionally add the print page to the site navigation
        if self.config.get("add_to_navigation"):
            nav.items.append(self.print_page)
            nav.pages.append(self.print_page)

        return nav

    def on_page_content(self, html, page, config, files, **kwargs):

        # Save each page HTML *before* a template is applied inside the page class
        if page != self.print_page:
            page.html = html

        return html

    def on_page_context(self, context, page, config, nav):

        # Save the page context
        # We'll use the same context of the last rendered page
        # And apply it to the print page as well (in on_post_build event)
        self.context = context

    def on_post_build(self, config):

        # Combine the HTML of all pages present in the navigation
        self.print_page.content = self.renderer.write_combined()

        # Get the info for MkDocs to be able to apply a theme template on our print page
        env = config["theme"].get_env()
        template = env.get_template("main.html")
        self.context["page"] = self.print_page

        # Render the theme template and insert additional JS / CSS
        html = template.render(self.context)
        html = self.renderer.insert_js_css_statements(html)

        # Write the file to the output folder
        write_file(
            html.encode("utf-8", errors="xmlcharrefreplace"),
            self.print_page.file.abs_dest_path,
        )
