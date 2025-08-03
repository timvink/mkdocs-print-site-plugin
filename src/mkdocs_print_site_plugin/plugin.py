import logging
import os
import re
import sys
import functools
import re as regex_module


from mkdocs.config import config_options
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.utils import copy_file, get_relative_url, write_file

from mkdocs_print_site_plugin.renderer import Renderer
from mkdocs_print_site_plugin.urls import is_external
from mkdocs_print_site_plugin.utils import get_theme_name

logger = logging.getLogger("mkdocs.plugins")

HERE = os.path.dirname(os.path.abspath(__file__))


class PrintSitePlugin(BasePlugin):
    """
    MkDocs Plugin class for combining all site pages into a single page.
    """

    config_scheme = (
        ("add_to_navigation", config_options.Type(bool, default=False)),
        ("print_page_title", config_options.Type(str, default="Print Site")),
        ("print_page_basename", config_options.Type(str, default="print_page")),
        ("add_table_of_contents", config_options.Type(bool, default=True)),
        ("toc_title", config_options.Type(str, default=None)),
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

        # If the user does not specify a value for the item
        if self.config.get("toc_title") is None:
            self.config["toc_title"] = config.get(
                "mdx_configs", {}).get("toc", {}).get("title", "Table of Contents")

        # Because other plugins can alter the navigation
        # (and thus which pages should be in the print page)
        # it is important 'print-site' is defined last in the 'plugins'
        plugins = config.get("plugins")
        print_site_position = [*dict(plugins)].index("print-site")

        # Offset begins at 1 due to indexing starting at 0
        position_offset = 1

        # Check if 'hooks' is defined in the 'plugins' section
        if isinstance(config.get("hooks"), dict):
            position_offset += len(config.get("hooks"))

        if print_site_position != len(plugins) - position_offset:
            msg = "[mkdocs-print-site] 'print-site' should be defined as the *last* plugin,"
            msg += "to ensure the print page has any changes other plugins make."
            msg += "Please update the 'plugins:' section in your mkdocs.yml"
            logger.warning(msg)

        if "--dirtyreload" in sys.argv:
            msg = "[mkdocs-print-site] Note the 'print-site' page does render all pages "
            msg += "when using the --dirtyreload option."
            logger.warning(msg)

        # Get abs path to cover_page_template
        self.cover_page_template_path = ""
        if self.config.get("add_cover_page"):
            if self.config.get("cover_page_template") == "":
                self.cover_page_template_path = os.path.join(HERE, "templates", "cover_page.tpl")
            else:
                self.cover_page_template_path = os.path.join(
                    os.path.dirname(config.get("config_file_path")),
                    self.config.get("cover_page_template"),
                )
            if not os.path.exists(self.cover_page_template_path):
                msg = "[print-site-plugin]: Path specified in 'cover_page_template' not found."
                msg += "\nMake sure to use the URL relative to your mkdocs.yml file."
                logger.warning(msg)
                raise FileNotFoundError("File not found: %s" % self.cover_page_template_path)

        # Get abs path to print_site_banner_template
        self.banner_template_path = ""
        if self.config.get("add_print_site_banner"):
            if self.config.get("print_site_banner_template") == "":
                self.banner_template_path = os.path.join(HERE, "templates", "print_site_banner.tpl")
            else:
                self.banner_template_path = os.path.join(
                    os.path.dirname(config.get("config_file_path")),
                    self.config.get("print_site_banner_template"),
                )
            if not os.path.exists(self.banner_template_path):
                msg = "[print-site-plugin]: Path specified in 'print_site_banner_template' not found."
                msg += "\nMake sure to use the URL relative to your mkdocs.yml file."
                logger.warning(msg)
                raise FileNotFoundError("File not found: %s" % self.banner_template_path)

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

            config["extra_css"] = self.enum_css_files + config["extra_css"]

        # Create MkDocs Page and File instances
        self.print_file = File(
            path=self.config.get("print_page_basename") + ".md",
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

        # Link to the PDF version of the entire site on a page.
        if self.config.get("path_to_pdf") != "":
            pdf_url = self.config.get("path_to_pdf")
            if is_external(pdf_url):
                page.url_to_pdf = pdf_url
            else:
                page.url_to_pdf = get_relative_url(pdf_url, page.file.url)

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
            if config.get("extra_css"):
                self.context["extra_css"] = [
                    get_relative_url(f, self.print_page.file.url) for f in config.get("extra_css")
                ]
            if config.get("extra_javascript"):
                self.context["extra_javascript"] = [
                    get_relative_url(str(f), self.print_page.file.url) for f in config.get("extra_javascript")
                ]

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
            copy_file(os.path.join(os.path.join(HERE, "css"), "print-site.css"), css_file_path)

            # Add enumeration css
            for f in self.enum_css_files:
                f = f.replace("/", os.sep)
                css_file_path = os.path.join(config["site_dir"], f)
                copy_file(os.path.join(HERE, f), css_file_path)

            # Add theme CSS file
            css_file = "print-site-%s.css" % get_theme_name(config)
            if css_file in os.listdir(os.path.join(HERE, "css")):
                css_file_path = os.path.join(css_output_base_path, css_file)
                copy_file(os.path.join(os.path.join(HERE, "css"), css_file), css_file_path)

        # Combine the HTML of all pages present in the navigation
        self.print_page.content, self.print_page.toc = self.renderer.write_combined()

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
            html = config.get("plugins", {}).get("charts").add_javascript_variables(html, self.print_page, config)

        # Compatibility with mkdocs-drawio
        # As this plugin adds renderer html for every drawio diagram
        # referenced in your markdown files. This rendering happens
        # in the on_post_page event, which is skipped by this plugin
        # therefore we need to manual execute the drawio plugin renderer here.
        if config.get("plugins", {}).get("drawio"):
            html = config.get("plugins", {}).get("drawio").render_drawio_diagrams(html, self.print_page)

        # Compatibility with mkdocs-autorefs
        # As this plugin processes cross-references in the on_env event, 
        # which happens after the print page is generated, it's necessary to 
        # manually execute the autorefs fix_refs function here.
        autorefs_plugin = config.get("plugins", {}).get("mkdocs-autorefs") or config.get("plugins", {}).get("autorefs")
        if autorefs_plugin:
            from mkdocs_autorefs._internal.references import fix_refs
            
            # First, extract all available anchors from the HTML
            anchor_pattern = r'(?:id="([^"]+)"|name="([^"]+)")'
            anchor_matches = regex_module.findall(anchor_pattern, html, regex_module.IGNORECASE)
            available_anchors = set()
            for match in anchor_matches:
                # Each match is a tuple (id_value, name_value), one is empty
                anchor = match[0] or match[1]
                if anchor:
                    available_anchors.add(anchor)
            
            # Create custom url_mapper that converts cross-references to internal anchors
            def print_page_url_mapper(identifier, from_url=None):
                """
                Custom URL mapper for print page that converts all cross-references 
                to internal anchors in the same page instead of external URLs.
                """
                try:
                    # Get the original URL from autorefs
                    original_url, title = autorefs_plugin.get_item_url(identifier, from_url)
                    
                    # Check if identifier directly exists as anchor
                    if identifier in available_anchors:
                        return f"#{identifier}", title
                    
                    # Extract anchor part from URL if it exists
                    if '#' in original_url:
                        anchor = original_url.split('#')[-1]
                        
                        # Check if this anchor actually exists in the HTML
                        if anchor in available_anchors:
                            return f"#{anchor}", title
                        else:
                            # Try to find a similar anchor (case-insensitive, partial match)
                            anchor_lower = anchor.lower()
                            for available_anchor in available_anchors:
                                if (available_anchor.lower() == anchor_lower or 
                                    anchor_lower in available_anchor.lower() or 
                                    available_anchor.lower() in anchor_lower):
                                    return f"#{available_anchor}", title
                            
                            return f"#{anchor}", title  # Return original anchor anyway
                    else:
                        # If no anchor in original URL, try fuzzy matching with identifier
                        identifier_lower = identifier.lower()
                        for available_anchor in available_anchors:
                            if (available_anchor.lower() == identifier_lower or 
                                identifier_lower in available_anchor.lower() or 
                                available_anchor.lower() in identifier_lower):
                                return f"#{available_anchor}", title
                        
                        return f"#{identifier}", title  # Return anyway, might work
                        
                except Exception as e:
                    # Fallback: check if identifier exists as anchor or find fuzzy match
                    if identifier in available_anchors:
                        return f"#{identifier}", identifier
                    else:
                        # Try fuzzy matching as fallback
                        identifier_lower = identifier.lower()
                        for available_anchor in available_anchors:
                            if (available_anchor.lower() == identifier_lower or 
                                identifier_lower in available_anchor.lower()):
                                return f"#{available_anchor}", identifier
                        return f"#{identifier}", identifier  # Return anyway as last fallback
            
            # Apply cross-references to the HTML
            html, unmapped = fix_refs(
                html,
                print_page_url_mapper,
                link_titles=autorefs_plugin._link_titles,
                strip_title_tags=autorefs_plugin._strip_title_tags,
                _legacy_refs=autorefs_plugin.legacy_refs,
            )
            if unmapped:
                logger.warning(f"[mkdocs-print-site] Unmapped autorefs: {[ref for ref, _ in unmapped]}")

        # Compatibility with https://github.com/g-provost/lightgallery-markdown
        # This plugin insert link hrefs with double dashes, f.e.
        # <link href="//assets/css/somecss.css">
        # Details https://github.com/timvink/mkdocs-print-site-plugin/issues/68
        htmls = html.split("</head>")
        base_url = "../" if config.get("use_directory_urls") else ""
        htmls[0] = htmls[0].replace('href="//', f'href="{base_url}')
        htmls[0] = htmls[0].replace('src="//', f'src="{base_url}')
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
        write_file(html.encode("utf-8", errors="xmlcharrefreplace"), self.print_page.file.abs_dest_path)
