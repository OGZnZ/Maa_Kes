"""Assemble assets/ into the flat PI directory required by MaaFwApp build recipes.

MaaFwApp's pi-profile.yaml points to this directory: interface.json is sibling to resource/.
Runs both in CI and locally, idempotent (rebuilt cleanly each time).

Usage:
    python tools/ci/stage_pi_assets.py --tag v1.2.3 --rid MaaKes_android

Note: --rid only affects this staging directory (the interface.json included in the APK),
assets/interface.json in the repository is not modified; desktop rid remains MaaKes.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import jsonc

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "build-android" / "pi-assets"

# Top-level entries to copy into the PI directory, aligned with .github/android/pi-profile.yaml include list.
# agent/ is intentionally omitted: assets/interface.json agent section is commented out (PI does not declare an agent).
# If an agent is declared in the future, include list and recipes must be updated together.
ENTRIES = ("resource", "resource_TC", "tasks")


def stage(out_dir: Path, *, tag: str | None = None, rid: str | None = None) -> Path:
    assets = REPO_ROOT / "assets"
    if not (assets / "interface.json").is_file():
        raise SystemExit(f"assets/interface.json not found under {REPO_ROOT}")

    out_dir = out_dir.resolve()
    # Safety check: never allow clearing repo root or assets/ as staging output directory
    for protected in (REPO_ROOT.resolve(), assets.resolve()):
        if out_dir == protected:
            raise SystemExit(f"refusing to use {out_dir} as the staging directory")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    shutil.copy2(assets / "interface.json", out_dir / "interface.json")
    for entry in ENTRIES:
        shutil.copytree(assets / entry, out_dir / entry, dirs_exist_ok=True)
    shutil.copy2(REPO_ROOT / "LICENSE", out_dir / "LICENSE")

    interface_path = out_dir / "interface.json"
    with open(interface_path, encoding="utf-8") as handle:
        interface = jsonc.load(handle)

    if tag:
        interface["version"] = tag
    if rid:
        # APK upload uses a separate rid on MirrorChyan; the app update check reads rid from PI,
        # otherwise it would query desktop rid and fail to get Android assets (falling back to GitHub).
        interface["mirrorchyan_rid"] = rid

    with open(interface_path, "w", encoding="utf-8") as handle:
        jsonc.dump(interface, handle, ensure_ascii=False, indent=4)
        handle.write("\n")

    return interface_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory")
    parser.add_argument("--tag", default=None, help="Version string to write to interface.version")
    parser.add_argument(
        "--rid",
        default=None,
        help="Android rid to write to interface.mirrorchyan_rid; leave empty to keep original",
    )
    args = parser.parse_args()

    interface_path = stage(args.out, tag=args.tag, rid=args.rid)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(f"PI staged at {interface_path.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
