"""
"""

from typing import Any, Dict


def parse_triggers(yaml_content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses the 'trigger' section of an Azure Pipelines YAML.

    Parameters
    ----------
    yaml_content : Dict[str, Any]
        The loaded YAML content as a dictionary.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing trigger details, including branches and tags.
    """
    trigger = yaml_content.get("trigger", {})
    return {
        "branches": trigger.get("branches", {}).get("include", []),
        "tags": {
            "include": trigger.get("tags", {}).get("include", []),
            "exclude": trigger.get("tags", {}).get("exclude", []),
        },
    }
