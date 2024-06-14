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

def find_new_root( root, path):
    # Split the path by '/'
    path_parts = path.strip('/').split('/')
    
    # Recursive helper function
    def _find_node(current_node, parts):
        if not parts:
            return current_node
        
        # Get the next part of the path
        next_part = parts[0]
        
        # Look for the next node among the current node's children
        if not hasattr(current_node, 'children'):
            return None
        for child in current_node.children:
            if child.is_section:
                if child.title in next_part:
                    return _find_node(child, parts[1:])
        
        return None  # If the node is not found
    for node in root:
        if node.is_section:
            if node.title == path_parts[0]:
                return _find_node(node, path_parts[1:])
    
    return None
    
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
