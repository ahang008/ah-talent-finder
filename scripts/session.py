#!/usr/bin/env python3
"""ah-talent-finder session manager.

Handles all mechanical operations: folder creation, state tracking,
archive file writing, progress management. The AI reads this script's
JSON output and focuses on conversation + analysis.

Usage:
  python scripts/session.py check          # Check if session exists
  python scripts/session.py init           # Create archive folder + files
  python scripts/session.py reset          # Clear all session files
  python scripts/session.py status         # Print current progress
  python scripts/session.py progress --node "Step1-节点2"  # Update progress
  python scripts/session.py save --node "Step1-节点1" --field "基本面" \
      --content "身份：自由职业者\\n城市：南京"
  python scripts/session.py save-file --file "04-内心原密码报告.md" \
      --content "完整的报告内容..."
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── path resolution ──────────────────────────────────────────────

def _vault_root() -> Path:
    """Detect vault root from this script's location.

    .claude/skills/ah-talent-finder/scripts/session.py  ->  vault root
                       ^^^^^^^^^^^^^^^^^^^^  skill dir
    """
    return Path(__file__).resolve().parent.parent.parent.parent


def _archive_dir() -> Path:
    return _vault_root() / "📥 临时工作区" / "AI天赋发现"


def _session_file() -> Path:
    return _archive_dir() / ".session-state.json"


# ── node -> archive file mapping ─────────────────────────────────

NODE_FILE_MAP = {
    # Step1 nodes all write to 01-轻量画像.md
    "Step1-节点1": "01-轻量画像.md",
    "Step1-节点2": "01-轻量画像.md",
    "Step1-节点3": "01-轻量画像.md",
    "Step1-节点4": "01-轻量画像.md",
    "Step1-节点5": "01-轻量画像.md",
    "Step1-节点6": "01-轻量画像.md",
    "Step1-节点7": "01-轻量画像.md",
    "Step1-节点8": "01-轻量画像.md",
    # Step2 nodes
    "Step2-节点1": "02-过去信息摘要.md",
    "Step2-节点2": "03-内在信息摘要.md",
    "Step2-节点3": "04-内心原密码报告.md",
    # Step3
    "Step3-方向推荐": "05-职业方向清单.md",
    "Step3-验证方案": "06-验证行动清单.md",
    # Step4
    "Step4": "07-命理验证报告.md",
}

NODE_ORDER = [
    "Step1-节点1", "Step1-节点2", "Step1-节点3", "Step1-节点4",
    "Step1-节点5", "Step1-节点6", "Step1-节点7", "Step1-节点8",
    "Step2-节点1", "Step2-节点2", "Step2-节点3",
    "Step3-方向推荐", "Step3-验证方案",
    "Step4",
]

# ── state helpers ────────────────────────────────────────────────

def _load_state() -> dict:
    sf = _session_file()
    if sf.exists():
        return json.loads(sf.read_text(encoding="utf-8"))
    return {}


def _save_state(state: dict) -> None:
    _archive_dir().mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    _session_file().write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ── commands ─────────────────────────────────────────────────────

def cmd_check() -> None:
    """Print session existence + current node as JSON."""
    sf = _session_file()
    if not sf.exists():
        print(json.dumps({"has_session": False}))
        return

    state = _load_state()
    print(json.dumps({
        "has_session": True,
        "current_node": state.get("current_node", ""),
        "completed_nodes": state.get("completed_nodes", []),
        "path": state.get("path", "light"),
        "last_updated": state.get("last_updated", ""),
        "user": state.get("user", {}),
    }, ensure_ascii=False))


def cmd_init() -> None:
    """Create archive folder and all placeholder files."""
    ad = _archive_dir()
    ad.mkdir(parents=True, exist_ok=True)

    # README
    readme = ad / "README.md"
    if not readme.exists():
        readme.write_text(
            "# AI天赋发现\n\n"
            "本文件夹由AI天赋发现系统自动管理。\n"
            "所有对话存档保存在本地，不会上传到任何地方。\n",
            encoding="utf-8",
        )

    # Placeholder archive files
    for i in range(1, 8):
        f = ad / f"0{i}-轻量画像.md" if i == 1 else None
    filenames = [
        "01-轻量画像.md", "02-过去信息摘要.md", "03-内在信息摘要.md",
        "04-内心原密码报告.md", "05-职业方向清单.md",
        "06-验证行动清单.md", "07-命理验证报告.md",
    ]
    for fn in filenames:
        f = ad / fn
        if not f.exists():
            f.write_text("", encoding="utf-8")

    # Init session state
    _save_state({
        "current_node": "Step1-节点1",
        "completed_nodes": [],
        "path": "light",
        "user": {},
    })

    print(json.dumps({"status": "ok", "action": "initialized"}))


def cmd_reset() -> None:
    """Remove all session files, keep folder."""
    import shutil
    ad = _archive_dir()
    if ad.exists():
        shutil.rmtree(ad)
    print(json.dumps({"status": "ok", "action": "reset"}))


def cmd_status() -> None:
    """Human-readable progress display."""
    state = _load_state()
    if not state:
        print("无进行中的会话。")
        return

    cn = state.get("current_node", "未知")
    completed = state.get("completed_nodes", [])
    path = state.get("path", "light")
    user = state.get("user", {})

    print(f"当前节点: {cn}")
    print(f"已完成:   {', '.join(completed) if completed else '(无)'}")
    print(f"路径:     {'深度版' if path == 'deep' else '轻量版'}")
    if user:
        print(f"用户:     {user.get('name', '')} / {user.get('identity', '')} / {user.get('city', '')}")
    print(f"更新时间: {state.get('last_updated', '')}")


def cmd_progress(node: str) -> None:
    """Update current node in session state."""
    state = _load_state()
    if not state:
        print(json.dumps({"error": "no session, run init first"}))
        sys.exit(1)

    # Mark previous node as completed if not already
    prev = state.get("current_node", "")
    completed = state.get("completed_nodes", [])
    if prev and prev not in completed:
        completed.append(prev)

    state["current_node"] = node
    state["completed_nodes"] = completed
    _save_state(state)

    # Determine next node hint
    next_node = ""
    try:
        idx = NODE_ORDER.index(node)
        if idx + 1 < len(NODE_ORDER):
            next_node = NODE_ORDER[idx + 1]
    except ValueError:
        pass

    print(json.dumps({
        "status": "ok",
        "current_node": node,
        "next_node": next_node,
        "completed_count": len(completed),
    }, ensure_ascii=False))


def cmd_save(node: str, field: str, content: str, use_stdin: bool = False) -> None:
    """Append a field to the appropriate archive file."""
    if use_stdin:
        content = sys.stdin.read()
    state = _load_state()
    if not state:
        print(json.dumps({"error": "no session, run init first"}))
        sys.exit(1)

    filename = NODE_FILE_MAP.get(node)
    if not filename:
        print(json.dumps({"error": f"unknown node: {node}"}))
        sys.exit(1)

    filepath = _archive_dir() / filename

    # Build markdown block
    existing = filepath.read_text(encoding="utf-8") if filepath.exists() else ""

    block = f"\n## {field}\n\n{content}\n"

    # Avoid duplicate fields
    marker = f"\n## {field}\n"
    if marker in existing:
        # Replace existing field block
        parts = existing.split(marker, 1)
        before = parts[0]
        after = parts[1].split("\n## ", 1) if "\n## " in parts[1] else (parts[1], "")
        if isinstance(after, list) and len(after) > 1:
            existing = before + block + "## " + after[1]
        else:
            existing = before + block
    else:
        existing += block

    filepath.write_text(existing, encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "file": filename,
        "field": field,
    }, ensure_ascii=False))


def cmd_save_file(file: str, content: str, use_stdin: bool = False) -> None:
    """Overwrite an entire archive file with new content."""
    if use_stdin:
        content = sys.stdin.read()
    state = _load_state()
    if not state:
        print(json.dumps({"error": "no session, run init first"}))
        sys.exit(1)

    filepath = _archive_dir() / file
    filepath.write_text(content, encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "file": file,
        "size": len(content),
    }, ensure_ascii=False))


def cmd_set_path(path: str) -> None:
    """Set session path to 'light' or 'deep'."""
    if path not in ("light", "deep"):
        print(json.dumps({"error": "path must be 'light' or 'deep'"}))
        sys.exit(1)

    state = _load_state()
    state["path"] = path
    _save_state(state)
    print(json.dumps({"status": "ok", "path": path}))


def cmd_set_user(name: str = "", identity: str = "", city: str = "") -> None:
    """Update user info in session state."""
    state = _load_state()
    if not state:
        print(json.dumps({"error": "no session, run init first"}))
        sys.exit(1)

    user = state.get("user", {})
    if name:
        user["name"] = name
    if identity:
        user["identity"] = identity
    if city:
        user["city"] = city
    state["user"] = user
    _save_state(state)
    print(json.dumps({"status": "ok", "user": user}, ensure_ascii=False))


def cmd_read_file(file: str) -> None:
    """Print the contents of an archive file."""
    filepath = _archive_dir() / file
    if filepath.exists():
        print(filepath.read_text(encoding="utf-8"))
    else:
        print("")


def cmd_save_full_report(node: str, content: str, use_stdin: bool = False) -> None:
    """Save a full report (node 8, Step2-节点3, Step3 outputs) to the right file."""
    if use_stdin:
        content = sys.stdin.read()

    filename = NODE_FILE_MAP.get(node)
    if not filename:
        print(json.dumps({"error": f"unknown node: {node}"}))
        sys.exit(1)

    filepath = _archive_dir() / filename
    filepath.write_text(content, encoding="utf-8")
    # Update progress + path if deep
    state = _load_state()
    prev = state.get("current_node", "")
    completed = state.get("completed_nodes", [])
    if prev and prev not in completed:
        completed.append(prev)
    state["current_node"] = node
    state["completed_nodes"] = completed
    if node == "Step2-节点3":
        state["path"] = "deep"
    _save_state(state)

    print(json.dumps({
        "status": "ok",
        "file": filename,
        "size": len(content),
    }, ensure_ascii=False))


# ── CLI ──────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="ah-talent-finder session manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="Check if session exists (JSON output)")
    sub.add_parser("init", help="Create archive folder + placeholder files")
    sub.add_parser("reset", help="Delete all session files")
    sub.add_parser("status", help="Print human-readable progress")

    p = sub.add_parser("progress", help="Update current node")
    p.add_argument("--node", required=True, help="Node ID, e.g. Step1-节点2")

    p = sub.add_parser("save", help="Append a field to the archive file for this node")
    p.add_argument("--node", required=True)
    p.add_argument("--field", required=True)
    p.add_argument("--content", default="", help="Markdown content (or use --stdin)")
    p.add_argument("--stdin", action="store_true", help="Read content from stdin")

    p = sub.add_parser("save-file", help="Overwrite an entire archive file")
    p.add_argument("--file", required=True, help="Archive filename, e.g. 04-内心原密码报告.md")
    p.add_argument("--content", default="")
    p.add_argument("--stdin", action="store_true", help="Read content from stdin")

    p = sub.add_parser("save-report", help="Save a full report to the right archive file + update progress")
    p.add_argument("--node", required=True)
    p.add_argument("--content", default="")
    p.add_argument("--stdin", action="store_true", help="Read content from stdin")

    p = sub.add_parser("read-file", help="Print an archive file's contents")
    p.add_argument("--file", required=True)

    p = sub.add_parser("set-path", help="Set session path (light/deep)")
    p.add_argument("--path", required=True, choices=["light", "deep"])

    p = sub.add_parser("set-user", help="Update user info")
    p.add_argument("--name", default="")
    p.add_argument("--identity", default="")
    p.add_argument("--city", default="")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "check":
            cmd_check()
        elif args.command == "init":
            cmd_init()
        elif args.command == "reset":
            cmd_reset()
        elif args.command == "status":
            cmd_status()
        elif args.command == "progress":
            cmd_progress(args.node)
        elif args.command == "save":
            cmd_save(args.node, args.field, args.content, getattr(args, 'stdin', False))
        elif args.command == "save-file":
            cmd_save_file(args.file, args.content, getattr(args, 'stdin', False))
        elif args.command == "save-report":
            cmd_save_full_report(args.node, args.content, getattr(args, 'stdin', False))
        elif args.command == "read-file":
            cmd_read_file(args.file)
        elif args.command == "set-path":
            cmd_set_path(args.path)
        elif args.command == "set-user":
            cmd_set_user(args.name, args.identity, args.city)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
