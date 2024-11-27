"""
"""

from typing import Any, Dict, List


def parse_variables(yaml_content: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Parses the 'variables' section of an Azure Pipelines YAML.

    Parameters
    ----------
    yaml_content : Dict[str, Any]
        The loaded YAML content as a dictionary.

    Returns
    -------
    List[Dict[str, str]]
        A list of variables with their names and values.
    """
    variables = yaml_content.get("variables", [])
    parsed_variables = []

    for var in variables:
        if isinstance(var, dict):
            parsed_variables.append(
                {"name": var.get("name"), "value": var.get("value")}
            )
        elif isinstance(var, str):
            parsed_variables.append({"name": var, "value": None})
        else:
            raise ValueError(f"Unsupported variable format: {type(var)}")

    return parsed_variables
