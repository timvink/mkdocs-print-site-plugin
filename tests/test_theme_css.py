"""
Tests on the theme-specific print CSS files that are shipped with this plugin.
"""

import os
import re

CSS_DIR = os.path.join("src", "mkdocs_print_site_plugin", "css")


def read_css(theme_name):
    path = os.path.join(CSS_DIR, "print-site-%s.css" % theme_name)
    assert os.path.exists(path), "%s does not exist" % path
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_leading_comment(css):
    """
    Remove the header comment, so two CSS files can be compared on their rules only.
    """
    return re.sub(r"\A\s*/\*.*?\*/", "", css, count=1, flags=re.DOTALL).strip()


def test_materialx_css_matches_material():
    """
    mkdocs-materialx is a fork of mkdocs-material that registers itself under a
    different theme name, but ships the same templates and md-* classes.

    Because the print CSS is looked up by theme name, it needs its own copy.
    Keep the two files in sync.
    """
    assert strip_leading_comment(read_css("materialx")) == strip_leading_comment(read_css("material"))


def test_no_mkdocs_material_runtime_dependency():
    """
    mkdocs-material must not be a runtime dependency.

    It is not imported anywhere, and it makes it impossible to use forks like
    mkdocs-materialx, which install into the same 'material' package directory.

    See https://github.com/timvink/mkdocs-print-site-plugin/issues/149
    """
    with open("pyproject.toml", encoding="utf-8") as f:
        pyproject = f.read()

    dependencies = re.search(r"^dependencies\s*=\s*\[(.*?)\]", pyproject, flags=re.DOTALL | re.MULTILINE)
    assert dependencies is not None, "Could not find 'dependencies' in pyproject.toml"
    assert "mkdocs-material" not in dependencies.group(1)
