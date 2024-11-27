"""
"""

from typing import Any, Dict, List


def format_step_name(step: Dict[str, Any], index: int) -> str:
    """
    Determines a meaningful name for a step based on its attributes.

    Parameters
    ----------
    step : Dict[str, Any]
        The step definition.
    index : int
        The index of the step in the list.

    Returns
    -------
    str
        A meaningful name for the step.
    """
    # Use displayName or name if available
    if "displayName" in step:
        return step["displayName"]
    if "name" in step:
        return step["name"]

    # Derive the name based on the type of step
    if "script" in step:
        return f"bash... {step['script'].split()[-1]}"
    if "template" in step:
        return f"template: ... _{step['template'].split('/')[-1]}_"
    if "checkout" in step:
        return f"checkout: ... _{step['checkout']}_"

    # Default fallback
    return f"Step {index + 1}"


def extract_steps(job: Dict[str, Any]) -> List[str]:
    """
    Extracts and formats the steps from a job in a stage.

    Parameters
    ----------
    job : Dict[str, Any]
        The job definition containing steps.

    Returns
    -------
    List[str]
        A list of formatted step names.
    """
    steps = job.get("steps", [])
    return [format_step_name(step, index) for index, step in enumerate(steps)]
