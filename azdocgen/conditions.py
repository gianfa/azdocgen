"""
Module to parse and handle conditions in Azure Pipelines YAML.
"""

"""
Module to extract conditions from Azure Pipelines YAML files.
"""

from typing import Any, Dict, List, Union


def find_conditions(
    yaml_content: Union[Dict[str, Any], List[Any]], context: str = ""
) -> List[Dict[str, str]]:
    """
    Recursively extracts conditions from Azure Pipelines YAML.

    Parameters
    ----------
    yaml_content : Union[Dict[str, Any], List[Any]]
        The YAML content as a nested dictionary or list.
    context : str
        The context of the current level (e.g., "stage:BuildStage > job:BuildApp").

    Returns
    -------
    List[Dict[str, str]]
        A list of dictionaries with keys:
        - context: The hierarchical context where the condition is found.
        - condition: The condition string.
    """
    conditions = []

    if isinstance(yaml_content, dict):
        # Check for a `condition` key
        if "condition" in yaml_content:
            conditions.append(
                {"context": context, "condition": yaml_content["condition"]}
            )

        # Check for inline conditions (`- ${{ if ... }}`) in lists
        for key, value in yaml_content.items():
            new_context = f"{context} > {key}" if context else key
            conditions.extend(find_conditions(value, new_context))

    elif isinstance(yaml_content, list):
        for index, item in enumerate(yaml_content):
            # Handle inline conditions
            if isinstance(item, str) and item.strip().startswith("${{ if "):
                conditions.append(
                    {"context": f"{context} > item {index}", "condition": item.strip()}
                )
            else:
                conditions.extend(find_conditions(item, f"{context} > item {index}"))

    return conditions
