# AZDocGen: Azure Pipelines Documentation Generator 📜🚀

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
![publish workflow](https://github.com/gianfa/azdocgen/actions/workflows/publish.yml/badge.svg?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/azdocgen.svg)](https://pypi.org/project/azdocgen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AZDocGen is a Python-based tool to automatically generate detailed documentation for Azure Pipelines YAML files. It extracts key details, such as *triggers*, *variables*, *resources*, *stages*, *jobs*, *steps*, and *conditions*, and outputs structured Markdown documentation, including Mermaid diagrams for visual representation.

## Installation

You can install AZDocGen via `pip` or `poetry`.

### Using pip

```bash
pip install azdocgen
```

### Using Poetry

```bash
poetry add azdocgen
```

## Usage

### CLI Usage

You can use AZDocGen directly from the command line to generate documentation for an Azure Pipelines YAML file.

```bash
azdocgen <pipeline_yaml_path> <output_md_path>
```

#### Example

```bash
azdocgen azure-pipelines.yml docs/azure-pipelines-docs.md
```

This will parse the `azure-pipelines.yml` file and generate the documentation in the `docs/azure-pipelines-docs.md` file.

### Programmatic Usage

You can also use AZDocGen as a Python library to generate documentation programmatically.

#### Example

```python
import yaml
from azdocgen.generate_doc import generate_markdown
from azdocgen.triggers import parse_triggers
from azdocgen.variables import parse_variables
from azdocgen.resources import parse_resources
from azdocgen.stages import parse_stages

# Load the Azure Pipelines YAML file
pipeline_file = "azure-pipelines.yml"
output_file = "docs/azure-pipelines-docs.md"

with open(pipeline_file, "r") as f:
    yaml_content = yaml.safe_load(f)

# Parse the sections
triggers = parse_triggers(yaml_content)
variables = parse_variables(yaml_content)
resources = parse_resources(yaml_content)
stages = parse_stages(yaml_content)

# Generate Markdown documentation
generate_markdown(
    triggers=triggers,
    variables=variables,
    stages=stages,
    resources=resources,
    output_file=output_file,
    pipeline_file=pipeline_file,
)

print(f"Documentation written to {output_file}")
```

## Features

- **Triggers**: Extracts branch and tag triggers.
- **Variables**: Documents variables defined in the pipeline.
- **Resources**: Lists repositories, containers, and pipeline dependencies.
- **Stages, Jobs, and Steps**: Provides a hierarchical breakdown of the pipeline.
- **Conditions**: Includes all conditions at stage, job, and step levels.
- **Mermaid Diagrams**: Generates visual workflows.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m 'Add my feature'`.
4. Push to the branch: `git push origin feature/my-feature`.
5. Submit a pull request.

## License

AZDocGen is licensed under the MIT License. See `LICENSE` for more details.
