import pytest

from azdocgen.stages import parse_stages


@pytest.fixture
def sample_yaml():
    return {
        "stages": [
            {
                "stage": "build",
                "displayName": "Build Stage",
                "dependsOn": [],
                "jobs": [],
            },
            {
                "stage": "deploy",
                "displayName": "Deploy Stage",
                "dependsOn": ["build"],
                "jobs": [],
            },
        ]
    }


def test_parse_stages(sample_yaml):
    stages = parse_stages(sample_yaml)
    assert len(stages) == 2
    assert stages[0]["name"] == "build"
    assert stages[1]["dependsOn"] == ["build"]
