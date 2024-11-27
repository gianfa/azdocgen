"""
"""

import pytest

from azdocgen.resources import parse_resources


@pytest.fixture
def sample_resources():
    return {
        "resources": {
            "repositories": [
                {"repository": "shared-templates", "ref": "refs/heads/main"},
                {"repository": "microservice-repo", "ref": "refs/heads/develop"},
            ],
            "containers": [
                {
                    "container": "my-docker-container",
                    "image": "myregistry.azurecr.io/my-image:latest",
                }
            ],
            "pipelines": [
                {
                    "pipeline": "dependency-pipeline",
                    "source": "my-org/dependency-project",
                }
            ],
        }
    }


def test_parse_resources(sample_resources):
    resources = parse_resources(sample_resources)
    assert len(resources["repositories"]) == 2
    assert (
        resources["containers"][0]["image"] == "myregistry.azurecr.io/my-image:latest"
    )
    assert resources["pipelines"][0]["source"] == "my-org/dependency-project"
