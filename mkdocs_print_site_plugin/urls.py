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


def fix_internal_links(html, page_url):
    """
    Updates links to internal pages to anchor links.
    This ensures internal links all point to locations inside the print page. 

    Args:
        html (str): HTML of page
        page_url (str): URL of the page 

    Returns:
        html (str): HTML of part of the print page with working internal links
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

    # Loop over href links (example in https://regex101.com/r/rMAHrE/520)
    href_regex = re.compile(r"<a\s+([^>]*?\s+)?href=\"(.*?)\"", flags=re.IGNORECASE)
    matches = re.finditer(href_regex, html)

    for m in matches:
        url = m.group(2)
        if is_external(url):
            continue
        elif is_anchor(url):
            url = "#" + page_key + "-" + url[1:]
        else:
            url = url_to_anchor(url)

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

    return html
