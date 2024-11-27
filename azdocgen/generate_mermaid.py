import re
from typing import Any, Dict, List

from azdocgen.steps import extract_steps

STYLES: dict = {
    "SIMPLE": {
        "stage": "color:#020ef9;",
        "job": "color:#FF1493;",
        "step": "",
    },
}


def format_node_id(identifier: str) -> str:
    """
    Formats a string to be a valid Mermaid node ID.

    Parameters
    ----------
    identifier : str
        The identifier to format.

    Returns
    -------
    str
        A formatted string for Mermaid.
    """
    # Replace invalid characters with underscores
    return re.sub(r"[^\w]", "_", identifier)


def get_step_name(step: Dict[str, Any], step_index: int) -> str:
    """
    Determines the name for a step based on its attributes.

    Parameters
    ----------
    step : Dict[str, Any]
        The step definition.
    step_index : int
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

    # Handle step as a string (e.g., checkout: shared-templates)
    if isinstance(step, str):
        return step

    # Derive the name based on the type of step
    if "script" in step:
        return f"bash script ({step['script'].split()[-1]})"
    if "bash" in step:
        return f"bash script ({step['bash'].split()[-1]})"
    if "template" in step:
        return f"template ({step['template'].split('/')[-1]})"
    if "checkout" in step:
        return f"checkout ({step['checkout']})"

    # Default fallback
    return f"Step {step_index + 1}"


def sanitize_node_label(label: str) -> str:
    """
    Sanitizes the node label for Mermaid compatibility.

    Parameters
    ----------
    label : str
        The label to sanitize.

    Returns
    -------
    str
        A sanitized label suitable for Mermaid diagrams.
    """
    label = re.sub(r"[^\w\s:/-]", "", label)
    return label.strip()


def generate_mermaid(
    stages: List[Dict[str, Any]],
    stage_style: str = "color:#020ef9;",
    job_style: str = "color:#FF1493;",
    step_style: str = "",
) -> str:
    """
    Generates a Mermaid diagram for Azure Pipelines stages, jobs, and steps.

    Parameters
    ----------
    stages : List[Dict[str, Any]]
        Parsed stages section from the YAML file.
    stage_style : str, optional
        Mermaid style for stages.
    job_style : str, optional
        Mermaid style for jobs.
    step_style : str, optional
        Mermaid style for steps.

    Returns
    -------
    str
        A Mermaid diagram in Markdown format.
    """
    diagram = ["```mermaid", "graph TD"]

    # Apply styles for stages, jobs, and steps
    if stage_style:
        diagram.append(f"classDef stage {stage_style}")
    if job_style:
        diagram.append(f"classDef job {job_style}")
    if step_style:
        diagram.append(f"classDef step {step_style}")

    for stage in stages:
        stage_id = format_node_id(stage["name"])
        stage_label = sanitize_node_label(stage["displayName"])
        stage_node = f'{stage_id}["{stage_label}"]'
        diagram.append(stage_node + ":::stage")  # Apply stage style

        # Add jobs and steps
        for job in stage.get("jobs", []):
            job_id = format_node_id(f"{stage_id}_{job['displayName']}")
            job_label = sanitize_node_label(job["displayName"])
            diagram.append(
                f'{stage_id} --> {job_id}["{job_label}"]:::job'
            )  # Apply job style

            # Add steps as a chain
            steps = extract_steps(job)
            previous_step_id = None
            for step_index, step in enumerate(steps):
                step_name = sanitize_node_label(get_step_name(step, step_index))
                step_id = format_node_id(f"{job_id}_{step_name}")
                diagram.append(f'{step_id}["{step_name}"]:::step')  # Apply step style
                if previous_step_id:
                    diagram.append(f"{previous_step_id} --> {step_id}")
                else:
                    # First step connects to the job
                    diagram.append(f"{job_id} --> {step_id}")
                previous_step_id = step_id  # Update for the next iteration

    diagram.append("```")  # End Mermaid block
    return "\n".join(diagram)
