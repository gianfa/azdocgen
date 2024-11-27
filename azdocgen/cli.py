"""
"""

import click
import yaml

from azdocgen.generate_doc import generate_markdown
from azdocgen.resources import parse_resources
from azdocgen.stages import parse_stages
from azdocgen.triggers import parse_triggers
from azdocgen.variables import parse_variables


@click.command()
@click.argument("yaml_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def cli(yaml_file: str, output_file: str) -> None:
    """
    CLI to parse Azure Pipelines YAML and generate documentation.

    Parameters
    ----------
    yaml_file : str
        Path to the Azure Pipelines YAML file.
    output_file : str
        Path to the output Markdown file.
    """
    with open(yaml_file, "r") as f:
        yaml_content = yaml.safe_load(f)

    # Parse sections
    triggers = parse_triggers(yaml_content)
    variables = parse_variables(yaml_content)
    stages = parse_stages(yaml_content)
    resources = parse_resources(yaml_content)

    # Generate Markdown
    generate_markdown(
        triggers=triggers,
        variables=variables,
        stages=stages,
        resources=resources,
        output_file=output_file,
        pipeline_file=yaml_file,  # Pass the pipeline file path
    )

    click.echo(f"Documentation written to {output_file}")
