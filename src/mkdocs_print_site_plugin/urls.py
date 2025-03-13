"""
Deal with URLs.

Some brainstorming:

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
import html
from os.path import splitext
from urllib.parse import urlparse


def is_external(url):
    """
    Test if a url is external.
    """
    prefixes = ("http", "www", "mailto:", "tel:", "skype:", "ftp:")
    return url.startswith(prefixes)


def is_base64_image(url):
    """
    Test if a url is a base64 data image.
    """
    prefixes = "data:image"
    return url.startswith(prefixes)


def is_attachment(url):
    """
    If URL points to an attachment.
    """
    path = urlparse(url).path
    ext = splitext(path)[1]
    return ext not in ["", ".html", ".md"]


def get_page_key(page_url):
    """
    Get the page key.

    Used to prepend a unique key to internal anchorlinks,
    so when we combine all pages into one, we don't get conflicting (duplicate) URLs

    Works the same when use_directory_urls is set to true or false in mkdocs.yml

    Examples
        get_page_key('index.html') --> 'index'
        get_page_key('/') --> 'index'
        get_page_key('abc/') --> 'abc'
        get_page_key('abc.html') --> 'abc'

    Args:
        page_url (str): The MkDocs url of the page
    """
    page_key = page_url.lower().strip().rstrip("/").replace(".html", "").replace("/", "-").lstrip("-")
    if len(page_key) > 0:
        return page_key
    else:
        return "index"


def fix_href_links(page_html, page_key, page_url, directory_urls=False):
    """
    Changes internal href HTML links to (anchor) links within the print page.
    """
    # Loop over href links (example in https://regex101.com/r/rMAHrE/520)
    href_regex = re.compile(r"<a\s+([^>]*?\s+)?href=\"(.*?)\"", flags=re.IGNORECASE)
    matches = re.finditer(href_regex, page_html)

    for m in matches:
        url = m.group(2)
        url = html.unescape(url)

        if is_external(url):
            continue
        elif is_attachment(url):
            url = get_url_from_root(url, page_url)
            if directory_urls:
                url = os.path.join("..", url)
            if os.sep != "/":
                # For windows compat
                url = url.replace(os.sep, "/")
        elif url.startswith("#"):
            # This is an anchor link within a mkdocs page
            url = "#" + page_key + "-" + url[1:]
        else:
            # This is a link to another mkdocs page
            # url 'a/#anchor-link' becomes '#a-anchor-link'
            # url '../Section2' with page_url '/Chapter1/Section1/ becomes '/Chapter1/Section2/'

            url_from_root = get_url_from_root(url, page_url)

            # If there is an anchor appended, fix that also
            url_paths = url_from_root.split("#")
            assert len(url_paths) <= 2
            page_url_1 = url_paths[0]
            url = "#" + get_page_key(page_url_1)
            if len(url_paths) == 2:
                url += "-" + url_paths[1]

        # Insert back any HTML between '<a' and 'href=', like "class='id'"
        other_html = m.group(1)
        if other_html is None:
            new_string = '<a href="%s"' % (url)
        else:
            new_string = '<a %s href="%s"' % (other_html.rstrip(), url)

        page_html = page_html.replace(m.group(), new_string)

    return page_html


def update_anchor_ids(page_html, page_key):
    """
    Changes internal anchors to make sure they are unique within the print page.

    For example, changes all instances in pagename.html of id="#anchor" to id="#pagename-anchor"

    It does this only for the h1-h6 tags.
    """
    # Regex demo / tests: https://regex101.com/r/mlAPNH/3
    href_regex = re.compile(
        r"<([^\s]+).*?id=\"([^\"]*?)\".*?>",
        flags=re.IGNORECASE,
    )
    matches = re.finditer(href_regex, page_html)

    change_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "sup", "li"]
    for m in matches:
        tag_text = m.group(1)
        if tag_text not in change_tags:
            continue
        id_text = m.group(2)
        match_text = m.group()
        new_text = match_text.replace(id_text, page_key + "-" + id_text)

        page_html = page_html.replace(match_text, new_text)

    return page_html


def fix_tabbed_content(page_html, page_key):
    """
    Tabbed content have <input> and <label> that are linked.

    When combining multiple pages into one, name duplicates occur.

    So in the example:

    <input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio">
    <label for="__tabbed_1_1">C</label>

    we should change:
    - <input> id, and <label> for attribute, to contain the pagekey.
    - <input> name, to make sure it's unique on print site

    So basically:
    <input checked="checked" id="{page_key}__tabbed_1_1" name="{page_key}__tabbed_1" type="radio">
    <label for="{page_key}__tabbed_1_1">C</label>
    """
    regex = re.compile(r"(\<input.*?name=\")([^\"]*?)(\".*?\>)", re.I)
    page_html = re.sub(regex, rf"\g<1>{page_key}-\g<2>\g<3>", page_html)

    regex = re.compile(r"(\<input.*?id=\")([^\"]*?)(\".*?\>)", re.I)
    page_html = re.sub(regex, rf"\g<1>{page_key}-\g<2>\g<3>", page_html)

    regex = re.compile(r"(\<label.*?for=\")([^\"]*?)(\".*?\>)", re.I)
    page_html = re.sub(regex, rf"\g<1>{page_key}-\g<2>\g<3>", page_html)

    return page_html


def fix_image_src(page_html, page_url, directory_urls):
    """
    Update img src path for images displayed in print page.

    This is because flattening all pages into 1 print page will break any relative links.
    """
    # Loop over all images src attributes
    # Example regex https://regex101.com/r/PLUmZ7/2
    img_regex = re.compile(r"<img[^>]+src=\"([^\">]+)\"", flags=re.IGNORECASE)
    matches = re.finditer(img_regex, page_html)

    for m in matches:
        img_src = m.group(1)
        if is_external(img_src):
            continue
        elif is_base64_image(img_src):
            continue

        img_text = m.group()

        new_url = get_url_from_root(img_src, page_url)

        if directory_urls:
            new_url = os.path.join("..", new_url)

        # For windows compat
        if os.sep != "/":
            new_url = new_url.replace(os.sep, "/")

        new_text = img_text.replace(img_src, new_url)

        page_html = page_html.replace(img_text, new_text)

    return page_html


def get_url_from_root(target_link, current_page_url):
    """
    Updates a relative URL to be relative to the print-site page instead.

    The print-site page is located at the root of the site.
    """
    current_page_rootdir = os.path.dirname(current_page_url)
    new_url = os.path.normpath(os.path.join(current_page_rootdir, target_link))

    # For windows compat
    if os.sep != "/":
        new_url = new_url.replace(os.sep, "/")

    return new_url


def fix_internal_links(page_html, page_url, directory_urls, heading_number):
    """
    Updates links to internal pages to anchor links.

    This ensures internal links all point to locations inside the print page.
    See also https://www.mkdocs.org/user-guide/configuration/?#use_directory_urls

    Args:
        page_html (str): HTML of page
        page_url (str): URL of the page
        directory_urls (bool): Whether the mkdocs sites is using directory urls

    Returns:
        html (str): HTML of part of the print page with working internal links
    """
    page_key = get_page_key(page_url)

    try:
        page_html = fix_href_links(page_html, page_key, page_url, directory_urls)
        page_html = update_anchor_ids(page_html, page_key)
        page_html = fix_tabbed_content(page_html, page_key)
        page_html = fix_image_src(page_html, page_url, directory_urls)
    except:
        print(f"Could not fix page '{page_url}', please report an issue on github")
        raise

    # Finally, wrap the entire page in a section with an anchor ID
    page_html = (
        ('<section class="print-page" id="%s" heading-number="%s">' % (page_key, heading_number))
        + page_html
        + "</section>"
    )

    return page_html
