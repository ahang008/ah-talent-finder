#!/usr/bin/env python3
"""Session manager for the AI Talent Discovery System (ah-talent-finder).

Handles all mechanical operations so the AI can focus on conversation
and analysis rather than file I/O and state tracking.

Usage:
    python3 scripts/session.py check
    python3 scripts/session.py init
    python3 scripts/session.py reset
    python3 scripts/session.py status
    python3 scripts/session.py progress --node "Step1-节点2"
    python3 scripts/session.py save --node "Step1-节点1" \
        --field "基本面" --stdin < content.txt
    python3 scripts/session.py save-report --node "Step1-节点8" \
        --stdin < report.md
    python3 scripts/session.py read-file --file "01-轻量画像.md"
    python3 scripts/session.py set-user --name "..." --identity "..."
    python3 scripts/session.py set-path --path deep
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def _vault_root() -> Path:
    """Detect Obsidian vault root from this script's location.

    .claude/skills/ah-talent-finder/scripts/session.py  ->  vault root
    """
    return Path(__file__).resolve().parent.parent.parent.parent


def _archive_dir() -> Path:
    return _vault_root() / "📥 临时工作区" / "AI天赋发现"


def _session_file() -> Path:
    return _archive_dir() / ".session-state.json"


# ---------------------------------------------------------------------------
# Node-to-file mapping
# ---------------------------------------------------------------------------

# fmt: off
_NODE_FILE_MAP: dict[str, str] = {
    "Step1-节点1": "01-轻量画像.md",
    "Step1-节点2": "01-轻量画像.md",
    "Step1-节点3": "01-轻量画像.md",
    "Step1-节点4": "01-轻量画像.md",
    "Step1-节点5": "01-轻量画像.md",
    "Step1-节点6": "01-轻量画像.md",
    "Step1-节点7": "01-轻量画像.md",
    "Step1-节点8": "01-轻量画像.md",
    "Step2-节点1": "02-过去信息摘要.md",
    "Step2-节点2": "03-内在信息摘要.md",
    "Step2-节点3": "04-内心原密码报告.md",
    "Step3-方向推荐": "05-职业方向清单.md",
    "Step3-验证方案": "06-验证行动清单.md",
    "Step4": "07-命理验证报告.md",
}

_NODE_ORDER: list[str] = [
    "Step1-节点1", "Step1-节点2", "Step1-节点3", "Step1-节点4",
    "Step1-节点5", "Step1-节点6", "Step1-节点7", "Step1-节点8",
    "Step2-节点1", "Step2-节点2", "Step2-节点3",
    "Step3-方向推荐", "Step3-验证方案",
    "Step4",
]

_ARCHIVE_FILES: list[str] = [
    "01-轻量画像.md", "02-过去信息摘要.md", "03-内在信息摘要.md",
    "04-内心原密码报告.md", "05-职业方向清单.md",
    "06-验证行动清单.md", "07-命理验证报告.md",
]
# fmt: on


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    """Load session state from JSON file."""
    sf = _session_file()
    if sf.exists():
        return json.loads(sf.read_text(encoding="utf-8"))
    return {}


def _save_state(state: dict) -> None:
    """Persist session state to JSON file."""
    _archive_dir().mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    _session_file().write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _ok(**kwargs) -> str:
    """Format a success JSON response."""
    return json.dumps({"status": "ok", **kwargs}, ensure_ascii=False)


def _err(msg: str) -> str:
    """Format an error JSON response."""
    return json.dumps({"error": msg}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check() -> None:
    """Check whether a session exists, print state as JSON."""
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
    """Create archive directory and initialise all placeholder files."""
    ad = _archive_dir()
    ad.mkdir(parents=True, exist_ok=True)

    # README for the archive folder
    readme = ad / "README.md"
    if not readme.exists():
        readme.write_text(
            "# AI天赋发现\n\n"
            "本文件夹由 AI 天赋发现系统自动管理。\n"
            "所有对话存档保存在本地，不会上传到任何地方。\n",
            encoding="utf-8",
        )

    # Placeholder archive files
    for fn in _ARCHIVE_FILES:
        f = ad / fn
        if not f.exists():
            f.write_text("", encoding="utf-8")

    # Initial session state
    _save_state({
        "current_node": "Step1-节点1",
        "completed_nodes": [],
        "path": "light",
        "user": {},
    })

    print(_ok(action="initialized"))


def cmd_reset() -> None:
    """Remove all session files (archive directory is recreated on init)."""
    ad = _archive_dir()
    if ad.exists():
        shutil.rmtree(ad)
    print(_ok(action="reset"))


def cmd_status() -> None:
    """Print human-readable session progress."""
    state = _load_state()
    if not state:
        print("No active session.")
        return

    cn = state.get("current_node", "unknown")
    completed = state.get("completed_nodes", [])
    path = state.get("path", "light")
    user = state.get("user", {})

    print(f"Current node:  {cn}")
    print(f"Completed:     {', '.join(completed) if completed else '(none)'}")
    print(f"Path:          {'Deep' if path == 'deep' else 'Light'}")
    if user:
        print(f"User:          {user.get('name', '')} / "
              f"{user.get('identity', '')} / {user.get('city', '')}")
    print(f"Last updated:  {state.get('last_updated', '')}")


def cmd_progress(node: str) -> None:
    """Advance session progress to *node*."""
    state = _load_state()
    if not state:
        print(_err("No session. Run `init` first."))
        sys.exit(1)

    prev = state.get("current_node", "")
    completed: list[str] = state.get("completed_nodes", [])
    if prev and prev not in completed:
        completed.append(prev)

    state["current_node"] = node
    state["completed_nodes"] = completed
    _save_state(state)

    # Next node hint
    next_node = ""
    try:
        idx = _NODE_ORDER.index(node)
        if idx + 1 < len(_NODE_ORDER):
            next_node = _NODE_ORDER[idx + 1]
    except ValueError:
        pass

    print(json.dumps({
        "status": "ok",
        "current_node": node,
        "next_node": next_node,
        "completed_count": len(completed),
    }, ensure_ascii=False))


def cmd_save(node: str, field: str, content: str) -> None:
    """Append a named *field* to the archive file for *node*.

    If the field already exists in the file it is replaced in-place.
    """
    state = _load_state()
    if not state:
        print(_err("No session. Run `init` first."))
        sys.exit(1)

    filename = _NODE_FILE_MAP.get(node)
    if not filename:
        print(_err(f"Unknown node: {node}"))
        sys.exit(1)

    filepath = _archive_dir() / filename
    existing = filepath.read_text(encoding="utf-8") if filepath.exists() else ""

    # Build new block
    block = f"\n## {field}\n\n{content}\n"
    marker = f"\n## {field}\n"

    if marker in existing:
        parts = existing.split(marker, 1)
        before = parts[0]
        rest = parts[1].split("\n## ", 1)
        after = f"\n## {rest[1]}" if len(rest) > 1 else ""
        existing = before + block + after
    else:
        existing += block

    filepath.write_text(existing, encoding="utf-8")
    print(_ok(file=filename, field=field))


def cmd_save_file(file: str, content: str) -> None:
    """Overwrite *file* in the archive directory with *content*."""
    state = _load_state()
    if not state:
        print(_err("No session. Run `init` first."))
        sys.exit(1)

    filepath = _archive_dir() / file
    filepath.write_text(content, encoding="utf-8")
    print(_ok(file=file, size=len(content)))


def cmd_save_report(node: str, content: str) -> None:
    """Save a full report and advance progress atomically."""
    filename = _NODE_FILE_MAP.get(node)
    if not filename:
        print(_err(f"Unknown node: {node}"))
        sys.exit(1)

    filepath = _archive_dir() / filename
    filepath.write_text(content, encoding="utf-8")

    # Advance progress
    state = _load_state()
    prev = state.get("current_node", "")
    completed: list[str] = state.get("completed_nodes", [])
    if prev and prev not in completed:
        completed.append(prev)
    state["current_node"] = node
    state["completed_nodes"] = completed
    if node == "Step2-节点3":
        state["path"] = "deep"
    _save_state(state)

    print(_ok(file=filename, size=len(content)))


def cmd_read_file(file: str) -> None:
    """Print contents of an archive file to stdout."""
    filepath = _archive_dir() / file
    if filepath.exists():
        print(filepath.read_text(encoding="utf-8"))
    else:
        print("")


def cmd_set_path(path: str) -> None:
    """Set session path to *light* or *deep*."""
    if path not in ("light", "deep"):
        print(_err("Path must be 'light' or 'deep'."))
        sys.exit(1)

    state = _load_state()
    state["path"] = path
    _save_state(state)
    print(_ok(path=path))


def cmd_set_user(name: str = "", identity: str = "", city: str = "") -> None:
    """Update user metadata in session state."""
    state = _load_state()
    if not state:
        print(_err("No session. Run `init` first."))
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
    print(_ok(user=user))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Session manager for ah-talent-finder"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="Check if a session exists (JSON)")
    sub.add_parser("init", help="Create archive directory and files")
    sub.add_parser("reset", help="Delete all session data")
    sub.add_parser("status", help="Print human-readable progress")

    p = sub.add_parser("progress", help="Advance to the given node")
    p.add_argument("--node", required=True,
                   help="Node ID, e.g. Step1-节点2")

    p = sub.add_parser("save", help="Append a field to the node's archive file")
    p.add_argument("--node", required=True)
    p.add_argument("--field", required=True)
    p.add_argument("--content", default="",
                   help="Markdown content (or use --stdin)")
    p.add_argument("--stdin", action="store_true",
                   help="Read content from stdin")

    p = sub.add_parser("save-file", help="Overwrite an archive file")
    p.add_argument("--file", required=True,
                   help="Archive filename, e.g. 04-内心原密码报告.md")
    p.add_argument("--content", default="")
    p.add_argument("--stdin", action="store_true",
                   help="Read content from stdin")

    p = sub.add_parser("save-report",
                       help="Save a full report and advance progress")
    p.add_argument("--node", required=True)
    p.add_argument("--content", default="")
    p.add_argument("--stdin", action="store_true",
                   help="Read content from stdin")

    p = sub.add_parser("read-file", help="Print an archive file")
    p.add_argument("--file", required=True)

    p = sub.add_parser("set-path", help="Set session path")
    p.add_argument("--path", required=True, choices=["light", "deep"])

    p = sub.add_parser("set-user", help="Update user metadata")
    p.add_argument("--name", default="")
    p.add_argument("--identity", default="")
    p.add_argument("--city", default="")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Resolve --stdin content
    def _content(arg_val: str, use_stdin: bool) -> str:
        return sys.stdin.read() if use_stdin else arg_val

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
            cmd_save(args.node, args.field,
                     _content(args.content, getattr(args, 'stdin', False)))
        elif args.command == "save-file":
            cmd_save_file(args.file,
                          _content(args.content, getattr(args, 'stdin', False)))
        elif args.command == "save-report":
            cmd_save_report(args.node,
                            _content(args.content, getattr(args, 'stdin', False)))
        elif args.command == "read-file":
            cmd_read_file(args.file)
        elif args.command == "set-path":
            cmd_set_path(args.path)
        elif args.command == "set-user":
            cmd_set_user(args.name, args.identity, args.city)
    except Exception as exc:
        print(_err(str(exc)))
        sys.exit(1)


if __name__ == "__main__":
    main()
