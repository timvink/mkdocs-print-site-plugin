import os
import re
import logging
import sys

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.utils import write_file, copy_file, get_relative_url
from mkdocs.exceptions import PluginError

from mkdocs_print_site_plugin.renderer import Renderer
from mkdocs_print_site_plugin.utils import flatten_nav, get_theme_name
from mkdocs_print_site_plugin.urls import is_external

logger = logging.getLogger("mkdocs.plugins")

HERE = os.path.dirname(os.path.abspath(__file__))


class PrintSitePlugin(BasePlugin):
    """
    MkDocs Plugin class for combining all site pages into a single page.
    """

    config_scheme = (
        ("add_to_navigation", config_options.Type(bool, default=False)),
        ("print_page_title", config_options.Type(str, default="Print Site")),
        ("add_table_of_contents", config_options.Type(bool, default=True)),
        ("toc_title", config_options.Type(str, default="Table of Contents")),
        ("toc_depth", config_options.Type(int, default=3)),
        ("add_full_urls", config_options.Type(bool, default=False)),
        ("enumerate_headings", config_options.Type(bool, default=True)),
        ("enumerate_headings_depth", config_options.Type(int, default=6)),
        ("enumerate_figures", config_options.Type(bool, default=True)),
        ("add_cover_page", config_options.Type(bool, default=False)),
        ("cover_page_template", config_options.Type(str, default="")),
        ("add_print_site_banner", config_options.Type(bool, default=False)),
        ("print_site_banner_template", config_options.Type(str, default="")),
        ("path_to_pdf", config_options.Type(str, default="")),
        ("include_css", config_options.Type(bool, default=True)),
        ("enabled", config_options.Type(bool, default=True)),
        ("exclude", config_options.Type(list, default=[])),
    )

    def on_config(self, config, **kwargs):
        """
        Event trigger on config.

        See https://www.mkdocs.org/user-guide/plugins/#on_config.
        """
        if not self.config.get("enabled"):
            return config
        # Check valid table of contents depth
        assert self.config.get("toc_depth") >= 1
        assert self.config.get("toc_depth") <= 6
        assert self.config.get("enumerate_headings_depth") >= 1
        assert self.config.get("enumerate_headings_depth") <= 6

        # Because other plugins can alter the navigation
        # (and thus which pages should be in the print page)
        # it is important 'print-site' is defined last in the 'plugins'
        plugins = config.get("plugins")
        print_site_position = [*dict(plugins)].index("print-site")
        if print_site_position != len(plugins) - 1:
            msg = "[mkdocs-print-site] 'print-site' should be defined as the *last* plugin,"
            msg += "to ensure the print page has any changes other plugins make."
            msg += "Please update the 'plugins:' section in your mkdocs.yml"
            logger.warning(msg)

        if "--dirtyreload" in sys.argv:
            msg = (
                "[mkdocs-print-site] Note the 'print-site' page does render all pages "
            )
            msg += "when using the --dirtyreload option."
            logger.warning(msg)

        # Get abs path to cover_page_template
        self.cover_page_template_path = ""
        if self.config.get("add_cover_page"):
            if self.config.get("cover_page_template") == "":
                self.cover_page_template_path = os.path.join(
                    HERE, "templates", "cover_page.tpl"
                )
            else:
                self.cover_page_template_path = os.path.join(
                    os.path.dirname(config.get("config_file_path")),
                    self.config.get("cover_page_template"),
                )
            if not os.path.exists(self.cover_page_template_path):
                msg = "[print-site-plugin]: Path specified in 'cover_page_template' not found."
                msg += "\nMake sure to use the URL relative to your mkdocs.yml file."
                logger.warning(msg)
                raise FileNotFoundError(
                    "File not found: %s" % self.cover_page_template_path
                )

        # Get abs path to print_site_banner_template
        self.banner_template_path = ""
        if self.config.get("add_print_site_banner"):
            if self.config.get("print_site_banner_template") == "":
                self.banner_template_path = os.path.join(
                    HERE, "templates", "print_site_banner.tpl"
                )
            else:
                self.banner_template_path = os.path.join(
                    os.path.dirname(config.get("config_file_path")),
                    self.config.get("print_site_banner_template"),
                )
            if not os.path.exists(self.banner_template_path):
                msg = "[print-site-plugin]: Path specified in 'print_site_banner_template' not found."
                msg += "\nMake sure to use the URL relative to your mkdocs.yml file."
                logger.warning(msg)
                raise FileNotFoundError(
                    "File not found: %s" % self.banner_template_path
                )

        # Add pointer to print-site javascript
        config["extra_javascript"] = ["js/print-site.js"] + config["extra_javascript"]

        # Add pointer to theme specific css files
        if self.config.get("include_css"):
            file = "print-site-%s.css" % get_theme_name(config)
            if file in os.listdir(os.path.join(HERE, "css")):
                config["extra_css"] = ["css/%s" % file] + config["extra_css"]
            else:
                msg = f"[mkdocs-print-site] Theme '{get_theme_name(config)}' not yet supported\n"
                msg += "which means print margins and page breaks might be off. Feel free to open an issue!"
                logger.warning(msg)

            # Add pointer to print-site css files
            config["extra_css"] = ["css/print-site.css"] + config["extra_css"]

            # Enumeration CSS files
            self.enum_css_files = []

            if self.config.get('enumerate_headings'):
                self.enum_css_files += ["css/print-site-enum-headings1.css"]
            if self.config.get('enumerate_headings_depth') >= 2:
                self.enum_css_files += ["css/print-site-enum-headings2.css"]
            if self.config.get('enumerate_headings_depth') >= 3:
                self.enum_css_files += ["css/print-site-enum-headings3.css"]
            if self.config.get('enumerate_headings_depth') >= 4:
                self.enum_css_files += ["css/print-site-enum-headings4.css"]
            if self.config.get('enumerate_headings_depth') >= 5:
                self.enum_css_files += ["css/print-site-enum-headings5.css"]
            if self.config.get('enumerate_headings_depth') >= 6:
                self.enum_css_files += ["css/print-site-enum-headings6.css"]

            config["extra_css"] = self.enum_css_files + config["extra_css"]


        # Create MkDocs Page and File instances
        self.print_file = File(
            path="print_page.md",
            src_dir="",
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
            plugin_config=self.config,
            mkdocs_config=config,
            cover_page_template_path=self.cover_page_template_path,
            banner_template_path=self.banner_template_path,
            print_page=self.print_page,
        )

        # Tracker
        # to see if context has been extracted from
        # template context
        self.context = {}

        return config

    def on_nav(self, nav, config, files, **kwargs):
        """
        The nav event is called after the site navigation is created.

        Can be used to alter the site navigation.
        See https://www.mkdocs.org/user-guide/plugins/#on_nav.
        """
        if not self.config.get("enabled"):
            return nav

        # Save the (order of) pages and sections in the navigation before adding the print page
        self.renderer.items = nav.items
        self.all_pages_in_nav = flatten_nav(nav.items)

        # Optionally add the print page to the site navigation
        if self.config.get("add_to_navigation"):
            nav.items.append(self.print_page)
            nav.pages.append(self.print_page)

        return nav

    def on_page_content(self, html, page, config, files, **kwargs):
        """
        The page_content event is called after the Markdown text is rendered to HTML.

        (but before being passed to a template) and can be used to alter the HTML body of the page.
        See https://www.mkdocs.org/user-guide/plugins/#on_page_content.
        """
        if not self.config.get("enabled"):
            return html

        # Save each page HTML *before* a template is applied inside the page class
        if page != self.print_page:
            page.html = html

        # We need to validate that the first heading on each page is a h1
        # This is required for the print page table of contents and enumeration logic
        if self.config.get("add_table_of_contents") or self.config.get(
            "enumerate_headings"
        ):
            if page in self.all_pages_in_nav:
                match = re.search(r"\<h[0-6]", html)
                if match:
                    if not match.group() == "<h1":
                        msg = f"The page {page.title} ({page.file.src_path}) does not start with a level 1 heading."
                        msg += "This is required for print page Table of Contents and/or enumeration of headings."
                        raise AssertionError(msg)

        # Link to the PDF version of the entire site on a page.
        if self.config.get("path_to_pdf") != "":
            pdf_url = self.config.get("path_to_pdf")
            if is_external(pdf_url):
                page.url_to_pdf = pdf_url
            else:
                page.url_to_pdf = get_relative_url(
                    pdf_url, page.file.url
                )

        return html

    def on_page_context(self, context, page, config, nav, **kwargs):
        """
        The page_context event is called after the context for a page is created.

        It can be used to alter the context for that specific page only.
        See https://www.mkdocs.org/user-guide/plugins/#on_page_context.
        """
        if not self.config.get("enabled"):
            return

        # Save relative link to print page
        # This can be used to customize a theme and add a print button to each page
        page.url_to_print_page = self.print_file.url_relative_to(page.file)

    def on_template_context(self, context, template_name, config, **kwargs):
        """
        The template_context event is called immediately after the context is created
        for the subject template and can be used to alter the context for that specific template only.

        See https://www.mkdocs.org/dev-guide/plugins/#on_template_context
        """
        if not self.config.get("enabled"):
            return

        # Save the page context
        # We'll use the same context of the last rendered page
        # And apply it to the print page as well (in on_post_build event)

        # Note a theme can have multiple templates
        # Found a bug where in the mkdocs theme,
        # the "sitemap.xml" static template
        # has incorrect 'extra_css' and 'extra_js' paths
        # leading to breaking the print page
        # at random (when sitemap.xml was rendered last)
        # we're assuming here all templates have a 404.html template
        # print(f"\nName: {template_name}\nContext: {context.get('extra_css')}")
        if template_name == "404.html":
            self.context = context
            # Make sure paths are OK
            if config.get('extra_css'):
                self.context['extra_css'] = [get_relative_url(f, self.print_page.file.url) for f in config.get('extra_css')]
            if config.get('extra_javascript'):
                self.context['extra_javascript'] = [get_relative_url(str(f), self.print_page.file.url) for f in config.get('extra_javascript')]


    def on_post_build(self, config, **kwargs):
        """
        The post_build event does not alter any variables. Use this event to call post-build scripts.

        See https://www.mkdocs.org/user-guide/plugins/#on_post_build.
        """
        if not self.config.get("enabled"):
            return

        if len(self.context) == 0:
            msg = "Could not find a template context.\n"
            msg += "Report an issue at https://github.com/timvink/mkdocs-print-site-plugin\n"
            msg += f"And mention the template you're using: {get_theme_name(config)}"
            raise PluginError(msg)

        # Add print-site.js
        js_output_base_path = os.path.join(config["site_dir"], "js")
        js_file_path = os.path.join(js_output_base_path, "print-site.js")
        copy_file(os.path.join(os.path.join(HERE, "js"), "print-site.js"), js_file_path)

        if self.config.get("include_css"):
            # Add print-site.css
            css_output_base_path = os.path.join(config["site_dir"], "css")
            css_file_path = os.path.join(css_output_base_path, "print-site.css")
            copy_file(
                os.path.join(os.path.join(HERE, "css"), "print-site.css"), css_file_path
            )

            # Add enumeration css
            for f in self.enum_css_files:
                f = f.replace("/", os.sep)
                css_file_path = os.path.join(config["site_dir"], f)
                copy_file(
                    os.path.join(HERE, f), css_file_path
                )

            # Add theme CSS file
            css_file = "print-site-%s.css" % get_theme_name(config)
            if css_file in os.listdir(os.path.join(HERE, "css")):
                css_file_path = os.path.join(css_output_base_path, css_file)
                copy_file(
                    os.path.join(os.path.join(HERE, "css"), css_file), css_file_path
                )

        # Combine the HTML of all pages present in the navigation
        self.print_page.content = self.renderer.write_combined()
        # Generate a TOC sidebar for HTML version of print page
        self.print_page.toc = self.renderer.get_toc_sidebar()

        # Get the info for MkDocs to be able to apply a theme template on our print page
        env = config["theme"].get_env()
        # env.list_templates()
        template = env.get_template("main.html")
        self.context["page"] = self.print_page
        # Render the theme template for the print page
        html = template.render(self.context)

        # Remove lazy loading attributes from images
        # https://regex101.com/r/HVpKPs/1
        html = re.sub(r"(\<img.+)(loading=\"lazy\")", r"\1", html)        

        # Compatiblity with mkdocs-chart-plugin
        # As this plugin adds some javascript to every page
        # It should be included in the print site also
        if config.get("plugins", {}).get("charts"):
            html = (
                config.get("plugins", {})
                .get("charts")
                .add_javascript_variables(html, self.print_page, config)
            )

        # Compatibility with mkdocs-drawio
        # As this plugin adds renderer html for every drawio diagram
        # referenced in your markdown files. This rendering happens
        # in the on_post_page event, which is skipped by this plugin
        # therefore we need to manual execute the drawio plugin renderer here. 
        if config.get("plugins", {}).get("drawio"):
            html = (
                config.get("plugins", {})
                    .get("drawio")
                    .render_drawio_diagrams(html, self.print_page)
            )

        # Compatibility with https://github.com/g-provost/lightgallery-markdown
        # This plugin insert link hrefs with double dashes, f.e.
        # <link href="//assets/css/somecss.css">
        # Details https://github.com/timvink/mkdocs-print-site-plugin/issues/68
        htmls = html.split("</head>")
        base_url = "../" if config.get("use_directory_urls") else ""
        htmls[0] = htmls[0].replace("href=\"//", f"href=\"{base_url}")
        htmls[0] = htmls[0].replace("src=\"//", f"src=\"{base_url}")
        html = "</head>".join(htmls)

        # Determine calls to required javascript functions
        js_calls = "remove_material_navigation();"
        js_calls += "remove_mkdocs_theme_navigation();"
        if self.config.get("add_table_of_contents"):
            js_calls += "generate_toc();"

        # Inject JS into print page
        print_site_js = (
            """
        <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function () {
            %s
        })
        </script>
        """
            % js_calls
        )
        html = html.replace("</head>", print_site_js + "</head>")

        # Write the print_page file to the output folder
        write_file(
            html.encode("utf-8", errors="xmlcharrefreplace"),
            self.print_page.file.abs_dest_path,
        )
