"""把 assets/ 组装成 MaaFwApp 打包配方要的扁平 PI 目录。

MaaFwApp 的 pi-profile.yaml 指向这个目录：interface.json 与 resource/ 同级。
CI 与本地都能跑，幂等（每次都整体重建）。

用法:
    python tools/ci/stage_pi_assets.py --tag v1.2.3 --rid MaaKes_android

注意 --rid 只影响这个暂存目录（也就是进 APK 的那份 interface.json），
仓库里的 assets/interface.json 不会被改，桌面端的 rid 始终是 MaaKes。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import jsonc

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "build-android" / "pi-assets"

# 要拷进 PI 目录的顶层条目，与 .github/android/pi-profile.yaml 的 include 对齐。
# agent/ 故意不在里面：assets/interface.json 的 agent 段是注释状态（PI 未声明 agent），
# 带了也没人拉起。哪天 PI 真的声明了 agent，这里、include 和配方都要一起补。
ENTRIES = ("resource", "resource_TC", "tasks")


def stage(out_dir: Path, *, tag: str | None = None, rid: str | None = None) -> Path:
    assets = REPO_ROOT / "assets"
    if not (assets / "interface.json").is_file():
        raise SystemExit(f"assets/interface.json not found under {REPO_ROOT}")

    out_dir = out_dir.resolve()
    # 防手滑：绝不允许把仓库根或 assets/ 当成输出目录清掉
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
        # APK 上传到 MirrorChyan 的独立 rid；而 app 的更新检查读的是 PI 里的 rid，
        # 不改的话它会去查桌面那个 rid，拿不到 android 资源（会回退 GitHub 源）。
        interface["mirrorchyan_rid"] = rid

    with open(interface_path, "w", encoding="utf-8") as handle:
        jsonc.dump(interface, handle, ensure_ascii=False, indent=4)
        handle.write("\n")

    return interface_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="输出目录")
    parser.add_argument("--tag", default=None, help="写进 interface.version 的版本号")
    parser.add_argument(
        "--rid",
        default=None,
        help="写进 interface.mirrorchyan_rid 的 Android rid；留空则保持原值",
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
