from typing import Any, Dict, List

from azdocgen.generate_mermaid import generate_mermaid
from azdocgen.header import extract_header_tags
from azdocgen.steps import extract_steps


def generate_markdown(
    triggers: Dict[str, Any],
    variables: List[Dict[str, str]],
    stages: List[Dict[str, Any]],
    resources: Dict[str, List[Dict[str, Any]]],
    output_file: str,
    pipeline_file: str,
    title: str = "Azure Pipeline Documentation",
    badge_version: bool = True,
    include_workflow: bool = True,
    parameters: List[Dict[str, Any]] = None,
) -> None:
    """
    Generates a Markdown documentation file for Azure Pipelines YAML.

    Parameters
    ----------
    triggers : Dict[str, Any]
        Parsed triggers section from the YAML file.
    variables : List[Dict[str, str]]
        Parsed variables section from the YAML file.
    stages : List[Dict[str, Any]]
        Parsed stages section from the YAML file.
    resources : Dict[str, List[Dict[str, Any]]]
        Parsed resources section from the YAML file.
    output_file : str
        Path to the output Markdown file.
    pipeline_file : str
        Path to the Azure Pipelines YAML file.
    title : str
        The title of the documentation file.
    include_workflow : bool
        Whether to include a Mermaid diagram in the documentation.
    """
    # Extract header tags from the pipeline file
    header_tags = extract_header_tags(pipeline_file)

    # Use header title and description if available
    title = header_tags.get("@title", title)
    description = header_tags.get("@description", "")
    author = header_tags.get("@author", "Unknown")
    version = header_tags.get("@version", "N/A")

    with open(output_file, "w") as f:
        f.write(f"# {title}\n\n")

        # Add optional metadata
        if version != "N/A":
            if badge_version:
                f.write(
                    f"![Version](https://img.shields.io/badge/version-{version}-blue)\n\n"
                )
            else:
                f.write(f"**Version:** {version}\n\n")
        if author != "Unknown":
            f.write(f"**Author:** {author}\n\n")
        if description:
            f.write(f"{description}\n\n")

        # Triggers
        f.write("## Triggers\n")
        f.write(f"\nBranches: {', '.join(triggers.get('branches', []))}\n")
        f.write(
            f"\nTags Include: {', '.join(triggers.get('tags', {}).get('include', []))}\n"
        )
        if triggers.get("tags", {}).get("exclude"):
            f.write(f"Tags Exclude: {', '.join(triggers['tags']['exclude'])}\n")
        f.write("\n")

        # Parameters
        if parameters:
            f.write("## Parameters\n\n")
            for param in parameters:
                param_description = (
                    (" " + param["displayName"]) if param["displayName"] else ""
                )
                f.write(
                    f"- `{param['name']}`: (*{param['type']}*). Defaults to `{param['default']}`.{param_description}\n"
                )
            f.write("\n")

        # Variables
        f.write("## Variables\n\n")
        for var in variables:
            f.write(f"- `{var['name']}`: {var.get('value', 'No value')}\n")
        f.write("\n")

        # Resources
        f.write("## Resources\n\n")
        if resources.get("repositories"):
            for repo in resources["repositories"]:
                f.write(
                    f"- Repository: `{repo['repository']}` (ref: `{repo.get('ref', 'default')}`)\n"
                )
        if resources.get("containers"):
            for container in resources["containers"]:
                f.write(
                    f"- Container: `{container['container']}` ({container['image']})\n"
                )
        if resources.get("pipelines"):
            for pipeline in resources["pipelines"]:
                f.write(
                    f"- Pipeline: `{pipeline['pipeline']}` (Source: `{pipeline['source']}`)\n"
                )
        f.write("\n")

        # Stages
        f.write("## Stages\n\n")
        for stage in stages:
            f.write(f"- **{stage['name']}** ({stage['displayName']})\n\n")
            for job in stage.get("jobs", []):
                f.write(f"  - **Job: {job['displayName']}**\n")
                steps = extract_steps(job)
                if steps:
                    f.write("    - Steps:\n")
                    for step in steps:
                        f.write(f"      - {step}\n")
                else:
                    f.write("    - No steps defined\n")
            f.write("\n")

        # Include Mermaid Diagram
        if include_workflow:
            f.write("## Workflow Diagram\n\n")
            mermaid_diagram = generate_mermaid(stages)
            f.write(mermaid_diagram)
            f.write("\n")
