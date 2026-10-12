#!/usr/bin/env python3
"""Copy sdd project templates into a repository and report the detected stack.

Usage:
  init.py --target DIR --name NAME [--prototype APP] [--force] [--dry-run]

Existing files are skipped unless --force is given; every skipped file is
reported so the caller can merge it by hand. Output is line-oriented:
  CREATED <path> | OVERWROTE <path> | SKIPPED <path> | STACK <kind> <detail> | DIR <name>
"""
import argparse
import datetime
import json
import os
import shutil
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(PLUGIN_ROOT, "templates")


def render(text, values):
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_tree(src_root, dst_root, values, rename, force, dry_run):
    for dirpath, _, filenames in os.walk(src_root):
        for filename in sorted(filenames):
            src = os.path.join(dirpath, filename)
            rel = os.path.relpath(src, src_root)
            for old, new in rename.items():
                rel = rel.replace(old, new)
            dst = os.path.join(dst_root, rel)
            exists = os.path.exists(dst)
            if exists and not force:
                print(f"SKIPPED {rel}")
                continue
            if not dry_run:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(src, encoding="utf-8") as fh:
                    content = render(fh.read(), values)
                with open(dst, "w", encoding="utf-8") as fh:
                    fh.write(content)
            print(f"{'OVERWROTE' if exists else 'CREATED'} {rel}")


def detect_stack(root):
    pkg = os.path.join(root, "package.json")
    if os.path.isfile(pkg):
        try:
            with open(pkg, encoding="utf-8") as fh:
                data = json.load(fh)
            scripts = ",".join(sorted((data.get("scripts") or {}).keys()))
            workspaces = data.get("workspaces")
            print(f"STACK node scripts={scripts or '-'}" + (f" workspaces={workspaces}" if workspaces else ""))
        except ValueError:
            print("STACK node package.json-unparseable")
        for lock, manager in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun"), ("bun.lock", "bun"), ("package-lock.json", "npm")):
            if os.path.isfile(os.path.join(root, lock)):
                print(f"STACK node-manager {manager}")
                break
    markers = {
        "Cargo.toml": "rust",
        "pyproject.toml": "python",
        "setup.py": "python",
        "requirements.txt": "python",
        "go.mod": "go",
        "Makefile": "make",
        "justfile": "just",
        "Gemfile": "ruby",
        "pom.xml": "java-maven",
        "build.gradle": "java-gradle",
        "build.gradle.kts": "java-gradle",
        "Package.swift": "swift",
        "pubspec.yaml": "dart",
        "deno.json": "deno",
    }
    for marker, kind in markers.items():
        if os.path.isfile(os.path.join(root, marker)):
            print(f"STACK {kind} {marker}")
    workflows = os.path.join(root, ".github", "workflows")
    if os.path.isdir(workflows):
        names = sorted(n for n in os.listdir(workflows) if n.endswith((".yml", ".yaml")))
        print(f"STACK ci github-actions {','.join(names) or '-'}")
    for name in sorted(os.listdir(root)):
        if os.path.isdir(os.path.join(root, name)) and not name.startswith(".") and name not in ("node_modules", "target", "dist", "build", "venv", ".venv"):
            print(f"DIR {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--prototype", metavar="APP", help="also create designs/APP prototype protocol")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        sys.exit(f"target is not a directory: {target}")
    values = {"PROJECT_NAME": args.name, "DATE": datetime.date.today().isoformat()}

    copy_tree(os.path.join(TEMPLATES, "project"), target, values, {}, args.force, args.dry_run)
    if args.prototype:
        copy_tree(os.path.join(TEMPLATES, "prototype"), target, values, {"__APP__": args.prototype}, args.force, args.dry_run)
    detect_stack(target)


if __name__ == "__main__":
    main()
