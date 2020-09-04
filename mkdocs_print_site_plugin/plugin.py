from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os
import warnings

from pathlib import Path
from functools import wraps

from mkdocs.structure.files import File

from mkdocs_print_site_plugin.renderer import Renderer

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(HERE, "CSS")


def delete_file_on_exception(path):
    """
    Decorator for class methods that ensures 
    a clean exit by ensuring a given filepath is deleted
    """

    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if os.path.exists(path):
                    os.remove(path)
                raise

        return func_wrapper

    return tags_decorator


class PrintSitePlugin(BasePlugin):

    config_scheme = (
        ("add_to_navigation", config_options.Type(bool, default=True)),
        ("print_page_title", config_options.Type(str, default="Print Site")),
    )

    def on_config(self, config, **kwargs):

        # Create empty file in `docs/` directory
        self.print_file_path = Path(config.get("docs_dir"), "print_page.md")
        with self.print_file_path.open(mode="w", encoding="UTF8") as f:
            f.write("")

        # Append printpage to the end of the nav.
        # prevents INFO warning that 'print_page.md' is not in nav
        if config.get("nav"):
            config.get("nav").append({"Print": "print_page.md"})

        # Insert print CSS styles corresponding to current theme
        theme_name = config.get("theme").name
        theme_css_files = [Path(f).stem for f in os.listdir(TEMPLATES_DIR)]
        if theme_name not in theme_css_files:
            warnings.warn(
                "[mkdocs-print-site] Theme %s not yet supported, which means print margins and page breaks might be off."
                % theme_name
            )

        self.renderer = Renderer(theme_name=theme_name)

        return config

    # @delete_file_on_exception(self.print_file_path)
    def on_files(self, files, config, **kwargs):

        # Finds and moves the print file to be the last file.
        # This ensures we can capture all other page HTMLs
        # before inserting all of them into the print page.
        self.print_file = files.src_paths["print_page.md"]
        new_files = [f for f in files._files if f != self.print_file]
        new_files.append(self.print_file)
        files._files = new_files

        # Add plugin CSS files to files
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

    # @delete_file_on_exception(self.print_file_path)
    def on_nav(self, nav, config, files, **kwargs):

        # Give the print page a nice title
        self.print_page = self.print_file.page
        self.print_page.title = self.config.get("print_page_title")
        self.print_page.edit_url = ""  # No edit icon on the print page.

        # Save the (order of) pages in the navigation
        # Because other plugins can alter the navigation
        # it is important 'print-site' in defined last in the 'plugins'
        nav_pages = [p for p in nav.pages if p != self.print_page]
        self.renderer.pages = nav_pages

        # Optionally remove the print page from the navigation
        if not self.config.get("add_to_navigation"):
            nav.pages = [p for p in nav.pages if p is not self.print_page]
            nav.items = [p for p in nav.items if p is not self.print_page]

        return nav

    # @delete_file_on_exception(self.print_file_path)
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

    def on_post_build(self, config: config_options.Config, **kwargs):

        # Delete print markdown file
        if os.path.exists(self.print_file_path):
            os.remove(self.print_file_path)
        
