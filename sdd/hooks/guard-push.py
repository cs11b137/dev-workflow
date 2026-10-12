#!/usr/bin/env python3
"""PreToolUse guard: ask before `git push` inside an sdd-initialized repo.

A repo counts as sdd-initialized when `docs/development-workflow.md` exists at
or above the working directory. Outside such repos the hook stays silent.
"""
import json
import os
import re
import sys

PUSH = re.compile(r"(^|[;&|(]\s*|\s)git(\s+-[cC]\s+\S+)*\s+push\b")


def sdd_root(start):
    path = os.path.abspath(start or ".")
    while True:
        if os.path.isfile(os.path.join(path, "docs", "development-workflow.md")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    command = (event.get("tool_input") or {}).get("command") or ""
    if not PUSH.search(command):
        return
    if not sdd_root(event.get("cwd")):
        return
    force = re.search(r"\s(--force(-with-lease)?|-f)\b", command)
    reason = (
        "sdd 完成门：任务只创建本地 commit，push 需要用户针对当前任务明确授权"
        + ("（这是 force push，会改写远端历史）" if force else "")
        + "。确认本次推送已获授权后再批准。"
    )
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    main()
