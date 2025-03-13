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


def get_section_id(section_number: str) -> str:
    return f"section-{section_number.replace('.', '-')}"
