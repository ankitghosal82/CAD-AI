import json
from pathlib import Path

from cad_validator.models import DesignFeatures


def load_designs_from_json(path: str | Path) -> list[DesignFeatures]:
    input_path = Path(path)
    raw_data = json.loads(input_path.read_text(encoding="utf-8"))
    return [DesignFeatures.from_dict(item) for item in raw_data]
