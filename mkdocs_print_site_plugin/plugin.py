from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os

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

    # config_scheme = (("add_to_navigation", config_options.Type(bool, default=True)),)

    def on_config(self, config, **kwargs):

        # Create empty file in `docs/` directory
        self.print_file_path = Path(config.get("docs_dir"), "print_page.md")
        with self.print_file_path.open(mode="w", encoding="UTF8") as f:
            f.write("")

        self.renderer = Renderer()

        # Append printpage to nav.
        # prevents INFO warning that 'print_page.md' is not in nav
        if config.get("nav"):
            config.get("nav").append({"Print": "print_page.md"})

        # Add generic print styles
        config["extra_css"].append(os.path.join("css", "print_site.css"))

        # Insert print CSS styles corresponding to current theme
        # Downside: this is added to every page, not just print site page.
        # TODO: insert print CSS only to CSS page, by inserting into <head>:
        # <link href="css/print_site.css" rel="stylesheet">
        # <link href="css/{theme_name}.css" rel="stylesheet">
        theme_name = config.get("theme").name
        theme_css_files = [Path(f).stem for f in os.listdir(TEMPLATES_DIR)]
        if theme_name in theme_css_files:
            config["extra_css"].append(os.path.join("css", theme_name + ".css"))
        else:
            raise UserWarning(
                "[mkdocs-print-site] Theme %s not yet supported, which means print margins and page breaks might be off."
                % theme_name
            )

        return config

    # @delete_file_on_exception(self.print_file_path)
    def on_files(self, files, config):

        # Finds and moves the print file to be the last file.
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
        # TODO: make this an option
        self.print_page = self.print_file.page
        self.print_page.title = "Print Site"

        # Save the (order of) pages in the navigation
        nav_pages = [p for p in nav.pages if p != self.print_page]
        self.renderer.pages = nav_pages

        # Append print page
        nav_pages_with_printpage = nav_pages + [self.print_page]
        nav.pages = nav_pages_with_printpage
        nav.items = nav_pages_with_printpage

        return nav

    # @delete_file_on_exception(self.print_file_path)
    def on_page_content(self, html, page, config, files, **kwargs):

        # Note that we made sure print page is the last file to be processed in the on_files() event
        if page != self.print_page:
            # Save the page HTML inside the page class
            page.html = html
        else:
            # Write the combined HTML of all pages in the navigation
            html = self.renderer.write_combined()

        return html

    def on_post_build(self, config: config_options.Config, **kwargs) -> dict:

        # Delete print markdown file
        if os.path.exists(self.print_file_path):
            os.remove(self.print_file_path)
