import pytest

from mkdocs_print_site_plugin.utils import (
    generate_link_from,
)

def test_generate_link_from():
    """
    Test generate_link_from.
    """

    title = ''
    assert generate_link_from(title) == ''

    title = 'thisshouldstayunmodified'
    assert generate_link_from(title) == 'thisshouldstayunmodified'

    title = 'Separa-tors not in url'
    assert generate_link_from(title) == 'separatorsnotinurl'

    title = "Punctuation.not'in;url"
    assert generate_link_from(title) == 'punctuationnotinurl'

    title = 'AccéntèdChärsNotinUrl'
    assert generate_link_from(title) == 'accentedcharsnotinurl'
