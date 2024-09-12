import os


def get_theme_name(config) -> str:
    """
    Determine theme name from the config.

    Supports the case when using overrides (using theme: null)

    Args:
        config: mkdocs config object

    Returns:
        name (str): Name of the mkdocs theme used
    """
    name = config.get("theme").name
    custom_dirs = [os.path.basename(d) for d in config.get("theme").dirs]

    if name:
        return name
    elif "material" in custom_dirs:
        return "material"
    elif "mkdocs" in custom_dirs:
        return "mkdocs"
    else:
        return name


def flatten_nav(items):
    """
    Create a flat list of pages from a nested navigation.
    """
    pages = []

    for item in items:
        if item.is_page:
            pages.append(item)
        if item.is_section:
            pages += flatten_nav(item.children)
    return pages
