"""
Test that builds with different setting succeed.

Note that pytest offers a `tmp_path`.

You can reproduce locally with:

```python
%load_ext autoreload
%autoreload 2
import os
import tempfile
import shutil
from pathlib import Path
tmp_path = Path(tempfile.gettempdir()) / 'pytest-table-builder'
if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
os.mkdir(tmp_path)
```

"""

import re
import os
import shutil
import logging
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory
    
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    
    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project
        
    Returns:
        testproject_path (Path): Path to test project
    """

    assert os.path.exists(mkdocs_yml_path)
    
    testproject_path = output_path / "testproject"
    os.makedirs(testproject_path, exist_ok=True)

    # Create empty 'testproject' folder
    if os.path.exists(str(testproject_path)):
        logging.warning(
            """This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(str(testproject_path))

    # Copy correct mkdocs.yml file and our test 'docs/'
    yml_dir = os.path.dirname(mkdocs_yml_path)
    shutil.copytree(yml_dir, str(testproject_path))
    shutil.copyfile(mkdocs_yml_path, str(testproject_path / "mkdocs.yml"))

    assert os.path.exists(testproject_path / "mkdocs.yml")
    return testproject_path


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command
    
    Args:
        testproject_path (Path): Path to test project
    
    Returns:
        command: Object with results of command
    """

    cwd = os.getcwd()
    os.chdir(str(testproject_path))
    
    try:
        run = CliRunner().invoke(build_command, catch_exceptions=True)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise


def check_build(tmp_path, project_mkdocs, exit_code=0):
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/projects/%s" % project_mkdocs, tmp_path
    )
    result = build_docs_setup(tmp_proj)
    
    msg = "cwd: %s, result: %s, exception: %s, exc_info: %s" % (os.getcwd(), result, result.exception, result.exc_info)
    assert result.exit_code == exit_code, msg
    return tmp_proj


def check_text_in_page(tmp_proj, page_path, text):
    page = tmp_proj / "site" / page_path
    assert page.exists(), "%s does not exist" % page_path
    contents = page.read_text(encoding="utf-8")
    assert re.search(text, contents)


#### Tests ####


def test_basic_build(tmp_path):
    prj_path = check_build(tmp_path, "basic/mkdocs.yml")

    # Make sure all 3 pages are combined and present
    check_text_in_page(
        prj_path, "print_page/index.html", '<h1 id="index-homepage">Homepage'
    )
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="a-a">A<')
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="z-z">Z')


def test_basic_build2(tmp_path):
    prj_path = check_build(tmp_path, "basic/mkdocs_no_directory_urls.yml")

    # Make sure all 3 pages are combined and present
    check_text_in_page(
        prj_path, "print_page.html", '<h1 id="index-homepage">Homepage</h1>'
    )
    check_text_in_page(prj_path, "print_page.html", '<h1 id="a-a">A</h1>')
    check_text_in_page(prj_path, "print_page.html", '<h1 id="z-z">Z</h1>')


def test_basic_build3(tmp_path):
    prj_path = check_build(tmp_path, "basic/mkdocs_with_nav.yml")

    # Make sure all 3 pages are combined and present
    check_text_in_page(
        prj_path, "print_page/index.html", '<h1 id="index-homepage">Homepage</h1>'
    )
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="a-a">A</h1>')
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="z-z">Z</h1>')


def test_basic_build4(tmp_path):
    prj_path = check_build(tmp_path, "basic/mkdocs_with_nav_and_theme.yml")

    # Make sure all 3 pages are combined and present
    check_text_in_page(
        prj_path, "print_page/index.html", '<h1 id="index-homepage">Homepage</h1>'
    )
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="a-a">A</h1>')
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="z-z">Z</h1>')


def test_basic_build5(tmp_path):
    prj_path = check_build(tmp_path, "with_markdown_ext/mkdocs.yml")

    # Sample some of the pages and make sure they are present in print page
    check_text_in_page(prj_path, "print_page/index.html", "PyMdown Extensions")
    check_text_in_page(prj_path, "print_page/index.html", "Footnotes")
    check_text_in_page(prj_path, "print_page/index.html", "Page two")


def test_basic_build6(tmp_path):
    # this test mainly checks if adding subsection to the navigation does not break plugin
    prj_path = check_build(tmp_path, "basic/mkdocs_weird_nav.yml")

    # Make sure the subsection pages are also in the page.
    check_text_in_page(prj_path, "print_page/index.html", "Subsec 1")
    check_text_in_page(prj_path, "print_page/index.html", "Subsec 2")


def test_basic_build99(tmp_path):
    # This is a weird test, as the markdown extension toc permalink setting seems to persist across subsequent test runs..
    prj_path = check_build(tmp_path, "basic/mkdocs_toc_permalink.yml")

    # Make sure all 3 pages are combined and present
    check_text_in_page(
        prj_path, "print_page/index.html", '<h1 id="index-homepage">Homepage'
    )
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="a-a">A')
    check_text_in_page(prj_path, "print_page/index.html", '<h1 id="z-z">Z')