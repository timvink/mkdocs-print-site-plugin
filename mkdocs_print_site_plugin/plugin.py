from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os
import tempfile
import warnings

from pathlib import Path

from mkdocs.structure.files import File

from mkdocs_print_site_plugin.renderer import Renderer


HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(HERE, "css")


class PrintSitePlugin(BasePlugin):

    config_scheme = (
        ("add_to_navigation", config_options.Type(bool, default=True)),
        ("print_page_title", config_options.Type(str, default="Print Site")),
    )

    def on_config(self, config, **kwargs):

        # Because other plugins can alter the navigation 
        # (and thus which pages should be in the print page)
        # it is important 'print-site' is defined last in the 'plugins'
        plugins = config.get('plugins')
        print_site_position = [*dict(plugins)].index('print-site')
        if print_site_position != len(plugins) - 1:
            warnings.warn("[mkdocs-print-site] 'print-site' should be defined as the *last* plugin, to ensure the print page has any changes other plugins make. Please update the 'plugins:' section in your mkdocs.yml")
        
        # Create the (empty) print page file in temp directory
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, "print_page.md")
        f = open(tmp_path, "w")
        f.write("")
        f.close()
        assert os.path.exists(tmp_path)
        
        self.print_file = File(
            path="print_page.md",
            src_dir=tmp_dir,
            dest_dir=config["site_dir"],
            use_directory_urls=config.get('use_directory_urls'),
        )

        # Insert 'print page' to the end of the nav, if it exists
        # We'll optionally remove the print page from navigation later on
        # Because when nav is not defined, all files incl print_page are part of the nav
        if config.get('nav'):
            config.get("nav").append({"updated_later_on": "print_page.md"})

        # Warn if we don't have CSS styles corresponding to current theme
        theme_name = config.get("theme").name
        theme_css_files = [Path(f).stem for f in os.listdir(TEMPLATES_DIR)]
        if theme_name not in theme_css_files:
            warnings.warn(
                "[mkdocs-print-site] Theme %s not yet supported, which means print margins and page breaks might be off."
                % theme_name
            )

        self.renderer = Renderer(theme_name=theme_name)

        return config

    def on_files(self, files, config, **kwargs):

        # Appending makes sure the print file is the last (page) file.
        # This ensures we can capture all other page HTMLs
        # before inserting all of them into the print page.
        files.append(self.print_file)
        
        # Add all plugin CSS files to files directory
        # Note we only insert the relevant css files per theme into the print page file
        css_dest_dir = os.path.join(config["site_dir"], "css")

        for file in os.listdir(TEMPLATES_DIR):
            print_site_css = File(
                path=file,
                src_dir=TEMPLATES_DIR,
                dest_dir=css_dest_dir,
                use_directory_urls=False,
            )
            files.append(print_site_css)

        return files

    def on_nav(self, nav, config, files, **kwargs):

        # Save print file
        self.print_page = self.print_file.page
        self.print_page.title = self.config.get("print_page_title")
        self.print_page.edit_url = None # Ensure no edit icon on the print page.
        
        # Save the (order of) pages in the navigation
        nav_pages = [p for p in nav.pages if p != self.print_page]
        self.renderer.pages = nav_pages

        # Optionally remove the print page from the navigation
        if not self.config.get("add_to_navigation"):
            nav.pages = [p for p in nav.pages if p is not self.print_page]
            nav.items = [p for p in nav.items if p is not self.print_page]

        return nav

    def on_page_content(self, html, page, config, files, **kwargs):

        # Note that we made sure print page is the last file
        # to be processed in the on_files() event
        if page != self.print_page:
            # Save the page HTML inside the page class
            page.html = html
        else:
            # Write the combined HTML of all pages in the navigation
            html = self.renderer.write_combined()

        return html

    def on_post_page(self, output, page, config, **kwargs):

        # Here we make sure to insert our CSS for printing
        # only to the print site page.
        if page == self.print_page:
            output = self.renderer.insert_css_statements(output)

        return output
