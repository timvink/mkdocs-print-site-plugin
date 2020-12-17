from mkdocs_print_site_plugin.urls import fix_href_links, update_anchor_ids, fix_image_src


def test_fix_href_links():

    html = '<h1><a href="page.html#anchor-link">the link</a></h1>'
    result = '<h1><a href="#page-anchor-link">the link</a></h1>'
    assert fix_href_links(html, "this_page") == result

    html = '<a href="test"'
    result = '<a href="#test"'
    assert fix_href_links(html, "this_page") == result

    html = '<li><a href="a/">page a</a></li><li><a href="z/">page z</a></li>'
    result = '<li><a href="#a">page a</a></li><li><a href="#z">page z</a></li>'
    assert fix_href_links(html, "this_page") == result

    html = '<li><a class = "bla" href="z/">page z</a></li>'
    result = '<li><a class = "bla" href="#z">page z</a></li>'
    assert fix_href_links(html, "this_page") == result

    html = "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps"
    result = fix_href_links(html, "this_page")
    assert result == html


def test_update_anchor_ids():

    # Make sure no changes are made

    html = '<h1><a href="page.html#anchor-link">the link</a></h1>'
    assert update_anchor_ids(html, "this_page") == html

    html = '<a href="test"'
    assert update_anchor_ids(html, "this_page") == html

    html = '<li><a href="a/">page a</a></li><li><a href="z/">page z</a></li>'
    assert update_anchor_ids(html, "this_page") == html

    html = '<li><a class = "bla" href="z/">page z</a></li>'
    assert update_anchor_ids(html, "this_page") == html

    html = "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps"
    assert update_anchor_ids(html, "this_page") == html

    # Make sure changes are made

    html = '<h6 id="a-section-on-something">A Section on something</h6>'
    result = '<h6 id="this_page-a-section-on-something">A Section on something</h6>'
    assert update_anchor_ids(html, "this_page") == result


def test_fix_image_src():

    # Make sure no changes are made

    html = '<h1><a href="page.html#anchor-link">the link</a></h1>'
    assert fix_image_src(html, "this_page", True) == html

    html = '<a href="test"'
    assert fix_image_src(html, "this_page", True) == html

    html = '<li><a href="a/">page a</a></li><li><a href="z/">page z</a></li>'
    assert fix_image_src(html, "this_page", True) == html

    html = '<li><a class = "bla" href="z/">page z</a></li>'
    assert fix_image_src(html, "this_page", True) == html

    html = "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps"
    assert fix_image_src(html, "this_page", True) == html

    # Make sure changes are made
    html = '<img src="../appendix/table.png">'
    result = '<img src="../appendix/table.png">'
    assert fix_image_src(html, "this_page", False) == result

    result = '<img src="../../appendix/table.png">'
    assert fix_image_src(html, "this_page", True) == result

# def test_url_to_anchor():
#     assert url_to_anchor("") == "#"
#     assert url_to_anchor("/") == "#"
#     assert url_to_anchor("a.html") == "#a"
#     assert url_to_anchor("a/") == "#a"
#     assert url_to_anchor("section/a/") == "#section-a"
#     assert url_to_anchor("section/a.html") == "#section-a"
#     assert url_to_anchor("section/a.html#anchor") == "#section-a-anchor"


# def test_fix_internal_links():

#     page_url = "customization/"
#     directory_urls = True

#     html = "<td>Wraps the hero teaser (if available)</td>\n</tr>\n<tr>\n<td><code>htmltitle</code></td>\n<td>Wraps the <code><title></code> tag</td>\n</tr>\n<tr>\n<td><code>libs</code></td>\n<td>Wraps"
#     result = fix_internal_links(html, page_url, directory_urls)
#     assert result == html

# def test_fix_internal_links():
#     html = """
#     <div style="border:2px; border-style:solid; border-color:#000000; padding: 1em; margin-bottom: 1em">
#         <h3>Print Site Page</h3>
#         <p>First example with text surrounded by a red border. This example also has multiple lines.</p>
#     </div>
#     <ul>
#     <li><a href="a/">page a</a></li>
#     <li><a href="z/">page z</a></li>
#     <li><a class="bla" style="color: #132" href="page.html#anchor">anchor on page</a></li>
#     </ul>
#     <p>text</p>
#     <h1 id="z">Z</h1>
#     <p>text</p>
#     <h1 id="a">A</h1>
#     <p>text</p>
#     <h2 id="sub-one">sub one</h2>
#     <p>text</p>
#     <h2 id="sub-two">sub two</h2>
#     """

#     assert '<a href="#a">page a</a>' in fix_internal_links(html, page_url="a/")

# def sample_html():
#     return """
#         <div style="border:2px; border-style:solid; border-color:#000000; padding: 1em; margin-bottom: 1em">
#             <h3>Print Site Page</h3>
#             <p>First example with text surrounded by a red border. This example also has multiple lines.</p>
#         </div>
#         <ul>
#         <li><a href="a/">page a</a></li>
#         <li><a href="z/">page z</a></li>
#         <li><a class="bla" style="color: #132" href="page.html#anchor">anchor on page</a></li>
#         </ul>
#         <p>text</p>
#         <h1 id="z">Z</h1>
#         <p>text</p>
#         <h1 id="a">A</h1>
#         <p>text</p>
#         <h2 id="sub-one">sub one</h2>
#         <p>text</p>
#         <h2 id="sub-two">sub two</h2>
#         """
