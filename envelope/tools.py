from pathlib import Path
from typing import List


def list_files(path: str) -> List[Path]:
    import_folder = Path(path)
    assert import_folder.is_dir(), "Must be a folder."
    return [file for file in import_folder.glob("*.ofx")]
