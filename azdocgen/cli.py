"""CLI interface"""

import click
import yaml

from azdocgen import __version__
from azdocgen.generate_doc import generate_markdown
from azdocgen.parameters import parse_parameters
from azdocgen.resources import parse_resources
from azdocgen.stages import parse_stages
from azdocgen.triggers import parse_triggers
from azdocgen.variables import parse_variables


@click.command()
@click.version_option(version=__version__, prog_name="azdocgen")
@click.argument("yaml_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option(
    "--disable",
    multiple=True,
    type=click.Choice(
        ["triggers", "variables", "stages", "resources", "workflow", "parameters"],
        case_sensitive=False,
    ),
    help="Disables specific components (e.g., --disable variables). Can be used multiple times.",
)
def cli(yaml_file: str, output_file: str, disable: tuple) -> None:
    """
    CLI to parse Azure Pipelines YAML and generate documentation.

    Parameters
    ----------
    yaml_file : str
        Path to the Azure Pipelines YAML file.
    output_file : str
        Path to the output Markdown file.
    --disable : str (optional)
        Components to disable (triggers, variables, stages, resources). Can be used multiple times.

    Examples
    --------
    1. **Generate documentation with all components**:
       ```
       python script.py pipeline.yaml output.md
       ```

    2. **Exclude only variables from the documentation**:
       ```
       python script.py pipeline.yaml output.md --disable variables
       ```

    3. **Exclude multiple components (e.g., variables and resources)**:
       ```
       python script.py pipeline.yaml output.md --disable variables --disable resources
       ```

    4. **Exclude all components (results in minimal documentation)**:
       ```
       python script.py pipeline.yaml output.md --disable triggers --disable variables --disable stages --disable resources
       ```
    """
    with open(yaml_file, "r") as f:
        yaml_content = yaml.safe_load(f)

    # Parse sections, skipping the disabled ones
    triggers = None if "triggers" in disable else parse_triggers(yaml_content)
    parameters = None if "parameters" in disable else parse_parameters(yaml_content)
    variables = None if "variables" in disable else parse_variables(yaml_content)
    stages = None if "stages" in disable else parse_stages(yaml_content)
    resources = None if "resources" in disable else parse_resources(yaml_content)
    workflow = None if "workflow" in disable else True

    # Generate Markdown
    generate_markdown(
        triggers=triggers,
        variables=variables,
        stages=stages,
        resources=resources,
        output_file=output_file,
        pipeline_file=yaml_file,  # Pass the pipeline file path
        include_workflow=workflow,
        parameters=parameters,
    )

    click.echo(f"Documentation written to {output_file}")


if __name__ == "__main__":
    cli()
