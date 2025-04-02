"""Parse parameters from Azure Pipeline or Template YAML."""
from typing import Any, Dict, List


def normalize_parameters(raw: List[Any]) -> List[Dict[str, Any]]:
    """Normalize both compact and expanded parameter forms."""
    normalized = []
    for param in raw:
        if isinstance(param, dict) and "name" in param:
            # Expanded form
            normalized.append({
                "name": param["name"],
                "type": param.get("type", "any"),
                "default": param.get("default", "N/A"),
                "displayName": param.get("displayName", None)
            })
        elif isinstance(param, dict):
            # Compact form: { name: default }
            for k, v in param.items():
                normalized.append({
                    "name": k,
                    "type": "any",
                    "default": v,
                })
    return normalized


def parse_parameters(yaml_content: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_params = yaml_content.get("parameters", [])
    return normalize_parameters(raw_params)
