from mkdocs_print_site_plugin.exclude import exclude
import pytest

def test_exclude():

    with pytest.raises(AssertionError):
        exclude("fsdfs", "not a list")

    globs = ["index.md"]
    assert exclude("index.md", globs)

    globs = ["*.md"]
    assert exclude("index.md", globs)
    assert exclude("folder/index.md", globs)
    assert exclude("folder\\index.md", globs)

    globs = ["folder/*"]
    assert exclude("folder/index.md", globs)
    assert not exclude("subfolder/index.md", globs)