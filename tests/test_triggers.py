"""
"""

import pytest

from azdocgen.triggers import parse_triggers


@pytest.fixture
def sample_triggers():
    return {
        "trigger": {
            "branches": {
                "include": ["main"],
            },
            "tags": {"include": ["v*"], "exclude": ["beta*"]},
        }
    }


def test_parse_triggers(sample_triggers):
    triggers = parse_triggers(sample_triggers)
    assert triggers["branches"] == ["main"]
    assert "v*" in triggers["tags"]["include"]
    assert "beta*" in triggers["tags"]["exclude"]
