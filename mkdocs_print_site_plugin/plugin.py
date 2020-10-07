import os
import tempfile
import logging

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.utils import write_file, copy_file, get_relative_url, warning_filter

from mkdocs_print_site_plugin.renderer import Renderer

logger = logging.getLogger("mkdocs.plugins")
logger.addFilter(warning_filter)

HERE = os.path.dirname(os.path.abspath(__file__))


class PrintSitePlugin(BasePlugin):

    config_scheme = (
        ("add_to_navigation", config_options.Type(bool, default=True)),
        ("print_page_title", config_options.Type(str, default="Print Site")),
        ("add_table_of_contents", config_options.Type(bool, default=True)),
        ("add_full_urls", config_options.Type(bool, default=False)),
        ("enumerate_headings", config_options.Type(bool, default=False)),
        ("enumerate_figures", config_options.Type(bool, default=False)),
        ("add_cover_page", config_options.Type(bool, default=False)),
        ("cover_page_template", config_options.Type(str, default="")),
        ("path_to_pdf", config_options.Type(str, default="")),
    )

    def on_config(self, config, **kwargs):

        # Because other plugins can alter the navigation
        # (and thus which pages should be in the print page)
        # it is important 'print-site' is defined last in the 'plugins'
        plugins = config.get("plugins")
        print_site_position = [*dict(plugins)].index("print-site")
        if print_site_position != len(plugins) - 1:
            logger.warning(
                "[mkdocs-print-site] 'print-site' should be defined as the *last* plugin, to ensure the print page has any changes other plugins make. Please update the 'plugins:' section in your mkdocs.yml"
            )

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
                logger.warning(
                    "[print-site-plugin]: Path specified in 'cover_page_template' not found. Make sure to use the URL relative to your mkdocs.yml file."
                )
                raise FileNotFoundError(
                    "File not found: %s" % self.cover_page_template_path
                )

        # Create the (empty) print page file in temp directory
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, "print_page.md")
        f = open(tmp_path, "w")
        f.write("")
        f.close()
        assert os.path.exists(tmp_path)

        # Add pointer to print-site javascript
        config["extra_javascript"] = ["js/print-site.js"] + config["extra_javascript"]
        config["extra_javascript"] = ["js/print-site-instant-loading.js"] + config[
            "extra_javascript"
        ]

        # Add pointer to print-site css files
        config["extra_css"] = ["css/print-site.css"] + config["extra_css"]

        # Add pointer to theme specific css files
        file = "print-site-%s.css" % config.get("theme").name
        if file in os.listdir(os.path.join(HERE, "css")):
            config["extra_css"] = ["css/%s" % file] + config["extra_css"]
        else:
            logger.warning(
                "[mkdocs-print-site] Theme '%s' not yet supported, which means print margins and page breaks might be off. Feel free to open an issue!"
                % config.get("theme").name
            )

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
            plugin_config=self.config,
            mkdocs_config=config,
            cover_page_template_path=self.cover_page_template_path,
            print_page=self.print_page,
        )

        return config

    def on_nav(self, nav, config, files, **kwargs):

        # Save the (order of) pages and sections in the navigation before adding the print page
        self.renderer.items = nav.items

        # Optionally add the print page to the site navigation
        if self.config.get("add_to_navigation"):
            nav.items.append(self.print_page)
            nav.pages.append(self.print_page)

        return nav

    def on_page_content(self, html, page, config, files, **kwargs):
        
        # Save each page HTML *before* a template is applied inside the page class
        if page != self.print_page:
            page.html = html

        if self.config.get("path_to_pdf") != "":
            page.url_to_pdf = get_relative_url(self.config.get("path_to_pdf"), page.file.url)

        return html

    def on_page_context(self, context, page, config, nav):

        # Save the page context
        # We'll use the same context of the last rendered page
        # And apply it to the print page as well (in on_post_build event)
        self.context = context

        # Save relative link to print page
        # This can be used to customize a theme and add a print button to each page
        page.url_to_print_page = self.print_file.url_relative_to(page.file)

    def on_post_build(self, config):

        # Add print-site.js
        js_output_base_path = os.path.join(config["site_dir"], "js")
        js_file_path = os.path.join(js_output_base_path, "print-site.js")
        copy_file(os.path.join(os.path.join(HERE, "js"), "print-site.js"), js_file_path)

        # Add print-site.css
        css_output_base_path = os.path.join(config["site_dir"], "css")
        css_file_path = os.path.join(css_output_base_path, "print-site.css")
        copy_file(
            os.path.join(os.path.join(HERE, "css"), "print-site.css"), css_file_path
        )
        # Add theme CSS file
        css_file = "print-site-%s.css" % config.get("theme").name
        if css_file in os.listdir(os.path.join(HERE, "css")):
            css_file_path = os.path.join(css_output_base_path, css_file)
            copy_file(os.path.join(os.path.join(HERE, "css"), css_file), css_file_path)

        # Determine calls to required javascript functions
        js_calls = ""
        if config.get("theme").name == "material":
            js_calls += "change_material_theme('default');"
        if self.config.get("add_table_of_contents"):
            js_calls += "generate_toc();"

        # Add JS file for compatibility for mkdocs-material instant loading
        # note this is inserted to all mkdocs pages,
        # because each page can be the start of instant loading session
        js_instant_loading = (
            """
         // Subscribe functions for compatibility 
         // with mkdocs-material's instant loading feature
         
         body = document.getElementsByTagName('body')[0];
         mkdocs_material_site_color_theme = body.getAttribute('data-md-color-scheme');
                    
         if (
            typeof app !== "undefined" && 
            typeof app.document$ !== "undefined"
            ) {
            app.document$.subscribe(function() {
                if ( document.querySelector("#print-site-page") !== null ) {
                    %s
                } else {
                    // Make sure to change the color theme back!
                    if ( mkdocs_material_site_color_theme !== null ) {
                        change_material_theme(mkdocs_material_site_color_theme);   
                    }
                }
            })
         }
        """
            % js_calls
        )
        write_file(
            js_instant_loading.encode("utf-8", errors="xmlcharrefreplace"),
            os.path.join(js_output_base_path, "print-site-instant-loading.js"),
        )

        # Combine the HTML of all pages present in the navigation
        self.print_page.content = self.renderer.write_combined()

        # Get the info for MkDocs to be able to apply a theme template on our print page
        env = config["theme"].get_env()
        template = env.get_template("main.html")
        self.context["page"] = self.print_page
        # Render the theme template for the print page
        html = template.render(self.context)

        # Inject JS into print page
        print_site_js = (
            """
        <script type="text/javascript">
        window.addEventListener('load', function () {
            %s
        })
        </script>
        """
            % js_calls
        )
        html = html.replace("</body>", print_site_js + "</body>")

        # Write the print_page file to the output folder
        write_file(
            html.encode("utf-8", errors="xmlcharrefreplace"),
            self.print_page.file.abs_dest_path,
        )
