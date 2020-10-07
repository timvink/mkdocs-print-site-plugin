"""
Links to other external pages --> Do nothing
Links to other internal pages
  Translate: Direct links with pages to anchor links
  Translate: link+anchor to anchor links
Links to anchors 
    Translate: from #anchor to #page+anchor

So within a page: 
    Add a new anchor at the start of the page with a id="#pagename"
    id="#anchor" to id="#pagename-anchor"
    href="#anchor" to href="#pagename-anchor"
    href="a/" to href="#a"
    href="a/#anchor" to href="#a-anchor"`


# with use_directory_urls = True
[p.url for p in self.pages]
['', 'z/', 'a/']

# use_directory_urls = False
[p.url for p in self.pages]
['index.html', 'z.html', 'a.html']
"""

import re
import os

def is_external(url):
    return url.startswith("http") or url.startswith("www")


def is_anchor(url):
    return url.startswith("#")


def url_to_anchor(url):
    """
    Translates an internal URL to an anchor URL
    
    Examples:
    
    / -> #index
    index.html -> #index
    page/    -> page
    page.html#anchor -> #page-anchor
    section/page.html#anchor -> #section-page-anchor
    page/ -> #page
    page/#anchor-link -> #page-anchor-link

    Args:
        url (str): value of page.url
    """
    url = url.rstrip("/")
    url = url.replace(".html", "")
    url = url.replace("/", "-")
    url = url.replace("#", "-")
    url = url.replace("--", "-")

    if len(url) > 0:
        url = "#" + url
    else:
        url = "index"

    return url


def anchor_add_page(url, page_url):
    """
    Adds the page ID to anchor IDs.
    (name attributes on a tag, id attributes on h1-h6 tags)
    http://www.tagindex.net/html/link/a_name.html#:~:text=The%20A%20element%20defines%20an,element%20is%20set%20as%20follows.&text=Anchor%20names%20must%20be%20unique%20within%20a%20document.
    
    Examples for page.html
    
    #anchor -> #page-anchor
    #anchor-link -> #page-anchor-link

    Args:
        url ([type]): [description]
    """
    return "#" + page_url + url[1:]


def get_page_key(page_url):
    """
    Get the page key.
    
    Used to prepend a unique key to internal anchorlinks,
    so when we combine all pages into one, we don't get conflicting (duplicate) URLs
    
    Works the same when use_directory_urls is set to true or false in mkdocs.yml
    
    Examples
        get_page_key('index.html') --> 'homepage'
        get_page_key('/') --> 'homepage'
        get_page_key('abc/') --> 'abc'
        get_page_key('abc.html') --> 'abc'
    

    Args:
        page_url (str): The MkDocs url of the page
    """
    # Get the page key. For example
    # 'index.html' or '/' will be 'homepage'
    # 'abc.html' or 'abc/' will be 'abc'
    if len(page_url) > 0:
        page_key = (
            page_url.lower().strip().rstrip("/").replace(".html", "").replace("/", "-")
        )
    else:
        page_key = "index"

    return page_key


def fix_internal_links(html, page_url, directory_urls):
    """
    Updates links to internal pages to anchor links.
    This ensures internal links all point to locations inside the print page. 

    Args:
        html (str): HTML of page
        page_url (str): URL of the page 
        directory_urls (bool): Whether the mkdocs sites is using directory urls, see https://www.mkdocs.org/user-guide/configuration/?#use_directory_urls

    Returns:
        html (str): HTML of part of the print page with working internal links
    """

    page_key = get_page_key(page_url)

    # Loop over href links (example in https://regex101.com/r/rMAHrE/520)
    href_regex = re.compile(r"<a\s+([^>]*?\s+)?href=\"(.*?)\"", flags=re.IGNORECASE)
    matches = re.finditer(href_regex, html)

    for m in matches:
        url = m.group(2)
        if is_external(url):
            continue
        elif is_anchor(url):
            # This is an anchor link within a mkdocs page
            url = "#" + page_key + "-" + url[1:]
        else:
            # This is a link to another mkdocs page
            # url 'a/#anchor-link' should become '#a-anchor-link'
            url_from_root = os.path.normpath(os.path.join('/',url))
            url_paths = url_from_root[1:].split("#")
            assert len(url_paths) <= 2
            page_url = url_paths[0]
            url = '#' + get_page_key(page_url)
            if len(url_paths) == 2:
                url += "-" + url_paths[1]
            

        # Insert back any HTML between '<a' and 'href=', like "class='id'"
        other_html = m.group(1)
        if other_html is None:
            other_html = ""
        new_string = '<a %s href="%s"' % (other_html, url)
        
        html = html.replace(m.group(), new_string)

    # All instances of id="#anchor" to id="#pagename-anchor"
    # Loop over h1-h6 id definitions
    # Regex demo / tests: https://regex101.com/r/pE66Kg/1
    href_regex = re.compile(
        r"\<h[1-6].+id=\"([aA-zZ|0-9|\-|\_|\.|\:]+)\"", flags=re.IGNORECASE
    )
    matches = re.finditer(href_regex, html)

    for m in matches:
        heading_id = m.group(1)
        match_text = m.group()
        new_text = match_text.replace(heading_id, page_key + "-" + heading_id)

        html = html.replace(match_text, new_text)

    # Finally, insert new anchor for each page
    html = ('<section class="print-page" id="%s">' % page_key) + html + "</section>"

    ### Loop over all images src attributes
    # This fixes images in the print page.
    # Example regex https://regex101.com/r/TTRsVW/1
    img_regex = re.compile(
        r"\<img.+src=\"([aA-zZ|0-9|\-|\_|\.|\:|\/]+)\"", flags=re.IGNORECASE
    )
    matches = re.finditer(img_regex, html)

    for m in matches:
        img_src = m.group(1)
        if is_external(img_src):
            continue
        img_text = m.group()
        
        new_url = os.path.normpath(os.path.join(os.path.dirname(page_url), img_src))
        
        if directory_urls:
            new_url = '../' + new_url
            
        new_text = img_text.replace(img_src, new_url)

        html = html.replace(img_text, new_text)


    return html
