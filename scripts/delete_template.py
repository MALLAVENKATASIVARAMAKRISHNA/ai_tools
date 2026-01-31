#!/usr/bin/env python3
"""
AI Karyashala - Delete Template Script
=====================================
Usage:
    python3 delete_template.py --title "Code Understanding Method"
"""

import os
import re
import argparse
from datetime import datetime


# ---------------- Utilities ----------------

def read_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_html(filepath, content):
    backup_dir = os.path.join(os.path.dirname(filepath), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    backup_file = f"index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    backup_path = os.path.join(backup_dir, backup_file)

    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"📦 Backup created: {backup_path}")


def find_index_html():
    paths = [
        "index.html",
        "../index.html",
        "../../index.html"
    ]
    for p in paths:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None


# ---------------- Core Logic ----------------

def delete_template(html, title):
    pattern = r'(const\s+learningTemplates\s*=\s*\[)(.*?)(\n\s*\];)'
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        print("❌ learningTemplates array not found")
        return None, False

    array_body = match.group(2)

    template_pattern = rf'\{{[^{{}}]*title:\s*"{re.escape(title)}"[^{{}}]*\}},?'
    new_array, count = re.subn(template_pattern, '', array_body, flags=re.DOTALL)

    if count == 0:
        return html, False

    new_html = (
        html[:match.start(2)]
        + new_array.rstrip().rstrip(',')
        + html[match.end(2):]
    )

    return new_html, True


def update_template_count(html, decrement=1):
    pattern = r'(<div class="text-4xl md:text-5xl font-black mb-1">)(\d+)(</div>\s*<div class="text-sm opacity-80">Templates</div>)'
    match = re.search(pattern, html)

    if match:
        current = int(match.group(2))
        new = max(0, current - decrement)
        html = html[:match.start()] + match.group(1) + str(new) + match.group(3) + html[match.end():]
        print(f"📊 Template count updated: {current} → {new}")

    return html


# ---------------- Main ----------------

def main():
    parser = argparse.ArgumentParser(description="Delete Template by title")
    parser.add_argument("--title", required=True, help="Template title to delete")
    parser.add_argument("--html", help="Path to index.html")
    args = parser.parse_args()

    html_path = args.html or find_index_html()
    if not html_path:
        print("❌ index.html not found")
        return

    html = read_html(html_path)
    new_html, deleted = delete_template(html, args.title)

    if not deleted:
        print(f"⚠️ Template '{args.title}' not found")
        return

    new_html = update_template_count(new_html, 1)
    write_html(html_path, new_html)

    print(f"✅ Template '{args.title}' deleted successfully")


if __name__ == "__main__":
    main()
