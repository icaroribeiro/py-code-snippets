from typing import Any


class TgMapper:
    @staticmethod
    def request_to_domain_dict(raw_json: dict[str, Any]) -> dict[str, Any]:
        """Maps HTTP incoming request body payload to core system-executable dictionary format."""
        return raw_json
