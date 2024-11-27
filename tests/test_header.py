from azdocgen.header import extract_header_tags


def test_extract_header_tags(tmp_path):
    header_file = tmp_path / "header_test.yaml"
    header_file.write_text(
        """
    # @title: Example Pipeline
    # @description: This pipeline showcases basic
    #   features and functionality.
    # @author: DevOps Team
    # @version: 1.0
    """
    )

    extracted = extract_header_tags(header_file)
    assert extracted["@title"] == "Example Pipeline"
    assert (
        extracted["@description"]
        == "This pipeline showcases basic features and functionality."
    )
    assert extracted["@author"] == "DevOps Team"
    assert extracted["@version"] == "1.0"
