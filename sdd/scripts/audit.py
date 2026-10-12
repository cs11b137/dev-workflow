#!/usr/bin/env python3
"""Audit sdd docs: root AGENTS.md size, relative links and anchors, ID
definitions and references, leftover TODO(sdd) placeholders.

Usage: audit.py [--root DIR] [--max-agents-lines 80]

Exit code 1 when any ERROR is reported; WARN and INFO never fail the run.
"""
import argparse
import collections
import os
import re
import sys
import urllib.parse

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
ID = re.compile(r"\b([A-Z]{1,4})-?(\d{2,3})\b")
TODO = re.compile(r"TODO\(sdd\)")
SKIP_DIRS = {"node_modules", ".git", "target", "dist", "build", ".venv", "venv", "vendor", "generated"}


def slugify(text):
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def strip_fences(lines):
    inside = False
    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            yield number, line


def anchors_of(path, cache):
    if path not in cache:
        seen = collections.Counter()
        found = set()
        with open(path, encoding="utf-8") as fh:
            for _, line in strip_fences(fh.read().splitlines()):
                match = HEADING.match(line)
                if not match:
                    continue
                slug = slugify(match.group(2))
                found.add(slug if seen[slug] == 0 else f"{slug}-{seen[slug]}")
                seen[slug] += 1
        cache[path] = found
    return cache[path]


def markdown_files(root):
    targets = [os.path.join(root, "AGENTS.md"), os.path.join(root, "CLAUDE.md")]
    for base in ("docs", "designs"):
        top = os.path.join(root, base)
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(("_", "."))]
            if base == "designs" and os.path.relpath(dirpath, top).count(os.sep) > 0:
                continue
            targets += [os.path.join(dirpath, f) for f in filenames if f.endswith(".md")]
    return [t for t in targets if os.path.isfile(t)]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".")
    parser.add_argument("--max-agents-lines", type=int, default=80)
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    errors, warns, infos = [], [], []

    agents = os.path.join(root, "AGENTS.md")
    if not os.path.isfile(agents):
        errors.append("AGENTS.md: missing (run /sdd:init)")
    else:
        with open(agents, encoding="utf-8") as fh:
            count = len(fh.read().splitlines())
        if count > args.max_agents_lines:
            errors.append(f"AGENTS.md: {count} lines > {args.max_agents_lines}; move details into docs and keep a routing line")
    if not os.path.isfile(os.path.join(root, "docs", "development-workflow.md")):
        errors.append("docs/development-workflow.md: missing (run /sdd:init)")

    anchor_cache = {}
    definitions = collections.defaultdict(list)
    references = []
    todo_counts = {}

    for path in markdown_files(root):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        todos = len(TODO.findall(raw))
        if todos:
            todo_counts[rel] = todos
        for number, line in strip_fences(raw.splitlines()):
            for target in LINK.findall(line):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("<"):
                    continue
                file_part, _, anchor = target.partition("#")
                file_part = urllib.parse.unquote(file_part)
                dest = path if not file_part else os.path.normpath(os.path.join(os.path.dirname(path), file_part))
                if not os.path.exists(dest):
                    errors.append(f"{rel}:{number}: broken link -> {target}")
                    continue
                if anchor and os.path.isfile(dest) and dest.endswith(".md"):
                    if urllib.parse.unquote(anchor).lower() not in anchors_of(dest, anchor_cache):
                        errors.append(f"{rel}:{number}: missing anchor -> {target}")
            if line.lstrip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                first = cells[0].strip("`* ") if cells else ""
                first_match = ID.fullmatch(first)
                if first_match:
                    definitions[first].append(f"{rel}:{number}")
                for cell in cells[1:] if first_match else cells:
                    for match in ID.finditer(cell):
                        references.append((match.group(0), match.group(1), f"{rel}:{number}"))

    prefixes = {ID.fullmatch(key).group(1) for key in definitions}
    for key, places in sorted(definitions.items()):
        if len(places) > 1:
            errors.append(f"ID {key} defined more than once: {', '.join(places)}")
    expanded = set(definitions)
    for key in definitions:
        match = ID.fullmatch(key)
        expanded.add(f"{match.group(1)}{match.group(2)}")
        expanded.add(f"{match.group(1)}-{match.group(2)}")
    for token, prefix, place in references:
        if prefix in prefixes and token not in expanded:
            warns.append(f"{place}: reference to undefined ID {token}")

    for rel, count in sorted(todo_counts.items()):
        infos.append(f"{rel}: {count} TODO(sdd) placeholder(s) left")

    for label, items in (("ERROR", errors), ("WARN", warns), ("INFO", infos)):
        for item in items:
            print(f"{label} {item}")
    print(f"SUMMARY errors={len(errors)} warnings={len(warns)} todos={sum(todo_counts.values())} ids={len(definitions)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
