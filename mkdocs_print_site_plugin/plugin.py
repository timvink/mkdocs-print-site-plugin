from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import os
import tempfile
import logging

from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.utils import write_file
from mkdocs.exceptions import ConfigurationError

from mkdocs_print_site_plugin.renderer import Renderer


HERE = os.path.dirname(os.path.abspath(__file__))


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

        # Raise error when using instant loading
        if "features" in config.get("theme"):
            if "instant" in config.get("theme")["features"]:
                raise ConfigurationError(
                    "[mkdocs-print-site] plugin is not compatible with instant loading. Remove the theme feature 'instant' in your mkdocs.yml file, or disable this plugin."
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

        # Save instance of the print page renderer
        self.renderer = Renderer(
            insert_toc=self.config.get("add_table_of_contents"),
            insert_explain_block=True,
        )

        return config

    def on_files(self, files, config, **kwargs):

        # Add all plugin JS and CSS files to files directory
        # Note we only include the relevant css and js files per theme into the print page file
        # in renderer.py

        # Include necessary CSS files
        CSS_DIR = os.path.join(HERE, "css")
        css_dest_dir = os.path.join(config["site_dir"], "css")
        self.css_files = {}

        # Add base print page CSS that applies to all themes
        file = "print_site.css"
        self.css_files[file] = File(
            path=file, src_dir=CSS_DIR, dest_dir=css_dest_dir, use_directory_urls=False,
        )

        # Add CSS file corresponding to mkdocs theme
        file = "print-css-%s.css" % config.get("theme").name
        if file in os.listdir(CSS_DIR):
            self.css_files[file] = File(
                path=file,
                src_dir=CSS_DIR,
                dest_dir=css_dest_dir,
                use_directory_urls=False,
            )
        else:
            logging.warning(
                "[mkdocs-print-site] Theme %s not yet supported, which means print margins and page breaks might be off."
                % config.get("theme").name
            )

        # Include necessary JS files
        js_dest_dir = os.path.join(config["site_dir"], "js")
        JS_DIR = os.path.join(HERE, "js")
        self.js_files = {}

        # Add the table of contents file
        if self.config.get("add_table_of_contents"):
            file = "print-site-toc.js"
            self.js_files[file] = File(
                path=file,
                src_dir=JS_DIR,
                dest_dir=js_dest_dir,
                use_directory_urls=False,
            )

        # Add JS for dealing with mkdocs-material theme
        file = "print-site-material.js"
        if file in os.listdir(JS_DIR):
            self.js_files[file] = File(
                path=file,
                src_dir=JS_DIR,
                dest_dir=js_dest_dir,
                use_directory_urls=False,
            )

        # Add the css and js files to MkDocs files collection
        for file in self.css_files:
            files.append(self.css_files[file])
        for file in self.js_files:
            files.append(self.js_files[file])

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

        # Insert CSS and JS files
        for file in self.css_files:
            self.css_files[file].url = "css/" + self.css_files[file].url
            file_path = self.css_files[file].url_relative_to(self.print_file)
            html = self.renderer.insert_css(html, file_path)

        for file in self.js_files:
            self.js_files[file].url = "js/" + self.js_files[file].url
            file_path = self.js_files[file].url_relative_to(self.print_file)
            html = self.renderer.insert_js(html, file_path)

        # Write the file to the output folder
        write_file(
            html.encode("utf-8", errors="xmlcharrefreplace"),
            self.print_page.file.abs_dest_path,
        )
