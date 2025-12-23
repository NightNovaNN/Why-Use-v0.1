#!/usr/bin/env python3

import os
import sys
import json
import re

INDEX_DIR = ".whyuse"
INDEX_FILE = os.path.join(INDEX_DIR, "index.json")

def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_index(index):
    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

def tokenize(line):
    return re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", line.lower())

def index_file(path, index):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, start=1):
                for token in tokenize(line):
                    index.setdefault(token, {})
                    index[token].setdefault(path, [])
                    index[token][path].append(lineno)
    except Exception as e:
        print(f"skipped {path}: {e}")

def index_path(path):
    index = load_index()

    if os.path.isfile(path):
        index_file(path, index)
    else:
        for root, _, files in os.walk(path):
            for file in files:
                full = os.path.join(root, file)
                index_file(full, index)

    save_index(index)
    print(" indexing complete")

def search(keyword):
    index = load_index()
    keyword = keyword.lower()

    if keyword not in index:
        print(" keyword not found")
        return

    print(f" '{keyword}' found in:\n")
    for file, lines in index[keyword].items():
        uniq = sorted(set(lines))
        print(f"- {file}: {', '.join(map(str, uniq))}")

def clear():
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
        print(" index cleared")
    else:
        print("nothing to clear")

def main():
    if len(sys.argv) < 2:
        print("usage: whyuse <index|search|clear> [...]")
        return

    cmd = sys.argv[1]

    if cmd == "index" and len(sys.argv) == 3:
        index_path(sys.argv[2])
    elif cmd == "search" and len(sys.argv) == 3:
        search(sys.argv[2])
    elif cmd == "clear":
        clear()
    else:
        print("invalid command")

if __name__ == "__main__":
    main()
