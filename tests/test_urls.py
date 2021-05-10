import pytest

from mkdocs_print_site_plugin.urls import (
    fix_href_links,
    update_anchor_ids,
    fix_image_src,
    get_page_key,
    is_external,
    is_attachment,
)


def test_get_page_key():
    """
    Test page key.
    """
    assert get_page_key("index.html") == "index"
    assert get_page_key("/") == "index"
    assert get_page_key("abc/") == "abc"
    assert get_page_key("abc.html") == "abc"
    assert get_page_key("/folder/subfolder/index.html") == "folder-subfolder-index"


def test_is_external():
    """
    Test.
    """
    assert is_external("https://www.google.com")
    assert is_external("mailto:me@abc.com")
    assert not is_external("/index.html")
    assert not is_external("index.html")


def test_is_attachment():
    """
    Test.
    """
    assert is_attachment("/file.py")
    assert is_attachment("../files/file.xlsx")
    assert not is_attachment("https://www.google.com")
    assert not is_attachment("../")
    assert not is_attachment("../page/subpage.html#md")


def test_fix_href_links():
    """
    Test.
    """
    html = '<h1><a href="page.html#anchor-link">the link</a></h1>'
    result = '<h1><a href="#page-anchor-link">the link</a></h1>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<a href="test"'
    result = '<a href="#test"'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a href="a/">page a</a></li><li><a href="z/">page z</a></li>'
    result = '<li><a href="#a">page a</a></li><li><a href="#z">page z</a></li>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a class = "bla" href="z/">page z</a></li>'
    result = '<li><a class = "bla" href="#z">page z</a></li>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a class = "bla" href="#section">page z</a></li>'
    result = '<li><a class = "bla" href="#this_page-section">page z</a></li>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a class = "bla" href="../z.html#anchor">page z</a></li>'
    result = '<li><a class = "bla" href="#z-anchor">page z</a></li>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a class = "bla" href="z/#section">page z</a></li>'
    result = '<li><a class = "bla" href="#z-section">page z</a></li>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a class = "bla" href="../../../z.html">page z</a></li>'
    result = '<li><a class = "bla" href="#z">page z</a></li>'
    assert fix_href_links(html, "this_page", "/") == result

    html = '<li><a class = "bla" href="../Section1/#reference">page z</a></li>'
    result = '<li><a class = "bla" href="#chapter1-section1-reference">page z</a></li>'
    assert fix_href_links(html, "this_page", "/Chapter1/Section2/") == result

    html = "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps"  # noqa
    result = fix_href_links(html, "this_page", "/")
    assert result == html


def test_update_anchor_ids_noupdate():
    """
    Test.
    """
    # Make sure no changes are made
    htmls = [
        '<h1><a href="page.html#anchor-link">the link</a></h1>',
        '<a href="test"',
        '<li><a href="a/">page a</a></li><li><a href="z/">page z</a></li>',
        '<li><a class = "bla" href="z/">page z</a></li>',
        "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps",  # noqa
        '<h1>no "id" here</h1>',
        '<input id="hello">blabla</input>',
        '<input class="something" id="hello">blabla</input>',
    ]

    for html in htmls:
        assert update_anchor_ids(html, "this_page") == html


@pytest.mark.parametrize("html_element", ["h1", "h2", "h3", "h4", "h5", "h6", "li", "sup"])
def test_update_anchor_ids(html_element):
    """
    Test changing ids.
    """
    html = '<%s id="a-section-on-something">A Section on something</%s>' % (html_element, html_element)
    result = '<%s id="this_page-a-section-on-something">A Section on something</%s>' % (html_element, html_element)
    assert update_anchor_ids(html, "this_page") == result

    # Make sure changes are made
    html = '<%s class="something" id="a-section-on-something">A Section on something</%s>' % (
        html_element,
        html_element,
    )
    result = '<%s class="something" id="this_page-a-section-on-something">A Section on something</%s>' % (
        html_element,
        html_element,
    )
    assert update_anchor_ids(html, "this_page") == result


def test_fix_image_src():
    """
    Test fixing image source.
    """
    # Make sure no changes are made

    html = '<h1><a href="page.html#anchor-link">the link</a></h1>'
    assert fix_image_src(html, "this_page", True) == html

    html = '<a href="test"'
    assert fix_image_src(html, "this_page", True) == html

    html = '<li><a href="a/">page a</a></li><li><a href="z/">page z</a></li>'
    assert fix_image_src(html, "this_page", True) == html

    html = '<li><a class = "bla" href="z/">page z</a></li>'
    assert fix_image_src(html, "this_page", True) == html

    html = "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps"  # noqa
    assert fix_image_src(html, "this_page", True) == html

    # Make sure absolute urls stay intct
    html = '<img src="/img.png">'
    assert fix_image_src(html, "this_page", False) == html

    # Make sure changes are made
    html = '<img src="../appendix/table.png">'
    result = '<img src="../appendix/table.png">'
    assert fix_image_src(html, "this_page", False) == result

    result = '<img src="../../appendix/table.png">'
    assert fix_image_src(html, "this_page", True) == result
