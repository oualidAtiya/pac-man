from pathlib import Path
import sys


def resource_path(relative_path: str) -> str:
    """Return the absolute path of a bundled resource.

    Args:
        relative_path: Path relative to the project root.

    Returns:
        The absolute path, valid both in development and in a
        PyInstaller build.
    """
    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir is not None:
        root = Path(bundle_dir)
    else:
        root = Path(__file__).resolve().parents[2]
    return str(root / relative_path)
