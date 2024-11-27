"""
"""

from typing import Any, Dict, List

import yaml


def parse_stages(yaml_content: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses the 'stages' section of an Azure Pipelines YAML.

    Parameters
    ----------
    yaml_content : Dict[str, Any]
        The loaded YAML content as a dictionary.

    Returns
    -------
    List[Dict[str, Any]]
        A list of stages with their details.
    """
    stages = yaml_content.get("stages", [])
    return [
        {
            "name": stage.get("stage"),
            "displayName": stage.get("displayName", stage.get("stage")),
            "dependsOn": stage.get("dependsOn", []),
            "jobs": stage.get("jobs", []),
        }
        for stage in stages
    ]
