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
from mkdocs_print_site_plugin.utils import flatten_nav, get_theme_name, find_new_root
from mkdocs_print_site_plugin.urls import is_external

logger = logging.getLogger("mkdocs.plugins")

HERE = os.path.dirname(os.path.abspath(__file__))
from mkdocs_print_site_plugin.exclude import exclude

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
        ("include", config_options.Type(list, default=["*"])),
        ("print_docs_dir", config_options.Type(str, default="")),
        ("pages_to_print", config_options.Type(list, default=[])),
    )
    page_renderers = {}
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

        def get_cover_page_template_path(config_data):
            cover_page_template_path=""
            if config_data["add_cover_page"]:
                if config_data["cover_page_template"] == "":
                    cover_page_template_path = os.path.join(
                        HERE, "templates", "cover_page.tpl"
                    )
                else:
                    cover_page_template_path = os.path.join(
                        os.path.dirname(config.get("config_file_path")),
                        config_data["cover_page_template"],
                    )
                if not os.path.exists(cover_page_template_path):
                    msg = "[print-site-plugin]: Path specified in 'cover_page_template' not found."
                    msg += "\nMake sure to use the URL relative to your mkdocs.yml file."
                    logger.warning(msg)
                    raise FileNotFoundError(
                        "File not found: %s" % cover_page_template_path
                    )
            return cover_page_template_path

        # Get abs path to print_site_banner_template
        def get_banner_template_path(config_data):
            banner_template_path = ""
            if config_data["add_print_site_banner"]:
                if config_data["print_site_banner_template"] == "":
                    banner_template_path = os.path.join(
                        HERE, "templates", "print_site_banner.tpl"
                    )
                else:
                    banner_template_path = os.path.join(
                        os.path.dirname(config.get("config_file_path")),
                        config_data["print_site_banner_template"],
                    )
                if not os.path.exists(banner_template_path):
                    msg = "[print-site-plugin]: Path specified in 'print_site_banner_template' not found."
                    msg += "\nMake sure to use the URL relative to your mkdocs.yml file."
                    logger.warning(msg)
                    raise FileNotFoundError(
                        "File not found: %s" % banner_template_path
                    )
            return banner_template_path
        
        def validate_page_entry(entry):
            if not isinstance(entry, dict): 
                raise ValueError("Each entry must be a dictionary.") 
            if "page_name" not in entry.keys() or "config" not in entry.keys(): 
                raise ValueError("Each entry must contain 'page' and 'config' keys.") 
            if not isinstance(entry["config"], list): 
                raise ValueError("The 'config' key must contain a list.")
            
        def convert_config_to_dict(config_list):
            return {list(detail.keys())[0]: list(detail.values())[0] for detail in config_list}

        def merge_config(default_config, custom_config):
            for key, value in default_config.items():
                if key not in custom_config:
                    custom_config[key] = value
            return custom_config
        

        # Create the default print_page
        global_page = {
                "page_name": "print_page",
                "config": {
                    "add_cover_page": self.config.get("add_cover_page"),
                    "cover_page_template" : self.config.get("cover_page_template"),
                    "exclude": self.config.get("exclude"),
                    "include": self.config.get("include"),
                    "add_to_navigation": self.config.get("add_to_navigation"),
                    "print_page_title" : self.config.get("print_page_title"),
                    "add_table_of_contents": self.config.get("add_table_of_contents"),
                    "toc_title" : self.config.get("toc_title"),
                    "toc_depth" : self.config.get("toc_depth"),
                    "add_full_urls": self.config.get("add_full_urls"),
                    "enumerate_headings": self.config.get("enumerate_headings"),
                    "enumerate_headings_depth" : self.config.get("enumerate_headings_depth"),
                    "enumerate_figures": self.config.get("enumerate_figures"),
                    "add_print_site_banner": self.config.get("add_print_site_banner"),
                    "print_site_banner_template" : self.config.get("print_site_banner_template"),
                    "path_to_pdf" : self.config.get("path_to_pdf"),
                    "include_css" : self.config.get("include_css"),
                    "enabled": self.config.get("enabled"),
                    "print_docs_dir" : self.config.get("print_docs_dir")
                }
            }

        pages_to_print = self.config.get("pages_to_print")
        self.print_pages={}
        ## Determine if pages_to_print is populated convert to print_pages or use default
        if isinstance(pages_to_print, list) and len(pages_to_print)>0: 
            for new_page in pages_to_print:
                #validate the data
                validate_page_entry(new_page)
                self.print_pages[new_page["page_name"]] =merge_config(
                                                            global_page['config'],
                                                            convert_config_to_dict(new_page["config"]))
        else:
        # If not add default single site content
            self.print_pages[global_page["page_name"]]=global_page['config']


        # Loop though the self.print_pages and 
        # convert the single page self._____ attribute storage 
        # to a self.print_pages[key]._____ attribute storage 
        
        # We'll address how to handle the returned config later.
        for page_name, page_config in self.print_pages.items():
            # Get abs path to cover_page_template
            #self.cover_page_template_path = get_cover_page_template_path(global_page['config'])
            page_config['cover_page_template_path'] = get_cover_page_template_path(page_config)

            # Get abs path to print_site_banner_template
            #self.banner_template_path = get_banner_template_path(global_page['config'])
            page_config['banner_template_path'] = get_banner_template_path(page_config)

            # Add pointer to print-site javascript
            config["extra_javascript"] = ["js/print-site.js"] + config["extra_javascript"]

            # Add pointer to theme specific css files
            # if self.config.get("include_css"):
            if page_config["include_css"]:
                file = "print-site-%s.css" % get_theme_name(config)
                if file in os.listdir(os.path.join(HERE, "css")):
                    config["extra_css"] = ["css/%s" % file] + config["extra_css"]
                else:
                    msg = f"[mkdocs-print-site] Theme '{get_theme_name(config)}' not yet supported\n"
                    msg += "which means print margins and page breaks might be off. Feel free to open an issue!"
                    logger.warning(msg)

                # Add pointer to print-site css files
                config["extra_css"] = ["css/print-site.css"] + config["extra_css"]

                # Add pointer to print-site css files
                config["extra_css"] = ["css/print-site.css"] + config["extra_css"]

                # Enumeration CSS files
                page_config['enum_css_files']=[]
                if page_config['enumerate_headings']:
                    page_config['enum_css_files'] += ["css/print-site-enum-headings1.css"]
                if page_config['enumerate_headings_depth'] >= 2:
                    page_config['enum_css_files'] += ["css/print-site-enum-headings2.css"]
                if page_config['enumerate_headings_depth'] >= 3:
                    page_config['enum_css_files'] += ["css/print-site-enum-headings3.css"]
                if page_config['enumerate_headings_depth'] >= 4:
                    page_config['enum_css_files'] += ["css/print-site-enum-headings4.css"]
                if page_config['enumerate_headings_depth'] >= 5:
                    page_config['enum_css_files'] += ["css/print-site-enum-headings5.css"]
                if page_config['enumerate_headings_depth'] >= 6:
                    page_config['enum_css_files'] += ["css/print-site-enum-headings6.css"]

                if page_config['enum_css_files'] not in config["extra_css"]:
                    config["extra_css"] = page_config['enum_css_files']+ config["extra_css"]
            # Create MkDocs Page and File instances
            page_config['print_file'] = File(
                path=f'{page_name}.md',
                src_dir="",
                dest_dir=config["site_dir"],
                use_directory_urls=config.get("use_directory_urls"),
            )
            page_config['print_page'] = Page(
                title=page_config["print_page_title"],
                file=page_config['print_file'],
                config=config,
            )
            page_config['print_page'].edit_url = None

            # Save instance of the print page renderer
            self.page_renderers[page_name] = Renderer(
                page_config=page_config,
                mkdocs_config=config,
                cover_page_template_path=page_config['cover_page_template_path'],
                banner_template_path=page_config['banner_template_path'],
                print_page=page_config['print_page'],
            )

            # Tracker
            # to see if context has been extracted from
            # template context
            page_config['context'] = {}
        return config
    


    def on_nav(self, nav, config, files, **kwargs):
        """
        The nav event is called after the site navigation is created.

        Can be used to alter the site navigation.
        See https://www.mkdocs.org/user-guide/plugins/#on_nav.
        """
        if not self.config.get("enabled"):
            return nav

        for page_name, page_config in self.print_pages.items():
            if not page_config['enabled']:
                continue
            # Save the (order of) pages and sections in the navigation before adding the print page
            print_dir=page_config['print_docs_dir']
            x = find_new_root(nav.items,print_dir )
            if hasattr(x, 'children'):
                self.page_renderers[page_name].items = x.children
                page_config['all_pages_in_nav'] = flatten_nav(x.children)
            else:
                self.page_renderers[page_name].items = x
                page_config['all_pages_in_nav'] = flatten_nav(x)


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
        html_pages = [val['print_page'] for k, val in self.print_pages.items()]
        
        for page_name, page_config in self.print_pages.items():
            if not page_config['enabled']:
                continue

            # Save each page HTML *before* a template is applied inside the page class
            # if page != self.print_page:
            #     page.html = html
            if page not in html_pages:
                page.html = html

            # Link to the PDF version of the entire site on a page.
            if page_config['path_to_pdf'] != "":
                pdf_url = page_config['path_to_pdf']
                if is_external(pdf_url):
                    page_config['url_to_pdf'] = pdf_url
                else:
                    page_config['url_to_pdf'] = get_relative_url(
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

        for page_name, page_config in self.print_pages.items():
            if not page_config['enabled']:
                continue
            # Save relative link to print page
            # This can be used to customize a theme and add a print button to each page
            page_config['url_to_print_page'] = page_config['print_file'].url_relative_to(page.file)

    def on_template_context(self, context, template_name, config, **kwargs):
        """
        The template_context event is called immediately after the context is created
        for the subject template and can be used to alter the context for that specific template only.

        See https://www.mkdocs.org/dev-guide/plugins/#on_template_context
        """
        if not self.config.get("enabled"):
            return
        
        for page_name, page_config in self.print_pages.items():
            if not page_config['enabled']:
                continue
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
                page_config['context'] = context
                # Make sure paths are OK
                if config.get('extra_css'):
                    page_config['context']['extra_css'] = [get_relative_url(f, page_config['print_page'].file.url) for f in config.get('extra_css')]
                if config.get('extra_javascript'):
                    page_config['context']['extra_javascript'] = [get_relative_url(str(f), page_config['print_page'].file.url) for f in config.get('extra_javascript')]


    def on_post_build(self, config, **kwargs):
        """
        The post_build event does not alter any variables. Use this event to call post-build scripts.

        See https://www.mkdocs.org/user-guide/plugins/#on_post_build.
        """
        if not self.config.get("enabled"):
            return

        for page_name, page_config in self.print_pages.items():
            if not page_config['enabled']:
                continue

            if len(page_config['context']) == 0:
                msg = "Could not find a template context.\n"
                msg += "Report an issue at https://github.com/timvink/mkdocs-print-site-plugin\n"
                msg += f"And mention the template you're using: {get_theme_name(config)}"
                raise PluginError(msg)

            # Add print-site.js
            js_output_base_path = os.path.join(config["site_dir"], "js")
            js_file_path = os.path.join(js_output_base_path, "print-site.js")
            copy_file(os.path.join(os.path.join(HERE, "js"), "print-site.js"), js_file_path)

            if page_config['include_css']:
                # Add print-site.css
                css_output_base_path = os.path.join(config["site_dir"], "css")
                css_file_path = os.path.join(css_output_base_path, "print-site.css")
                copy_file(
                    os.path.join(os.path.join(HERE, "css"), "print-site.css"), css_file_path
                )

                # Add enumeration css
                for f in page_config['enum_css_files']:
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
            page_config['print_page'].content = self.page_renderers[page_name].write_combined()
            # Generate a TOC sidebar for HTML version of print page
            page_config['print_page'].toc = self.page_renderers[page_name].get_toc_sidebar()

            # Get the info for MkDocs to be able to apply a theme template on our print page
            env = config["theme"].get_env()
            # env.list_templates()
            template = env.get_template("main.html")
            page_config['context']["page"] = page_config['print_page']
            # Render the theme template for the print page
            html = template.render(page_config['context'])

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
                    .add_javascript_variables(html, page_config['print_page, config'])
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
                        .render_drawio_diagrams(html, page_config['print_page'])
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
            if page_config['add_table_of_contents']:
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
                page_config['print_page'].file.abs_dest_path,
            )
