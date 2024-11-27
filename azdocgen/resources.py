"""
"""

from typing import Any, Dict, List


def parse_resources(yaml_content: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parses the 'resources' section of an Azure Pipelines YAML.

    Parameters
    ----------
    yaml_content : Dict[str, Any]
        The loaded YAML content as a dictionary.

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        A dictionary with keys 'repositories', 'containers', and 'pipelines',
        each containing a list of resources.
    """
    resources = yaml_content.get("resources", {})
    return {
        "repositories": resources.get("repositories", []),
        "containers": resources.get("containers", []),
        "pipelines": resources.get("pipelines", []),
    }
