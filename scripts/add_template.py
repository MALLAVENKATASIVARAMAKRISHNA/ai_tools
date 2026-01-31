#!/usr/bin/env python3
"""
AI Karyashala - Add New Template Script
========================================
This script adds a new learning template to the index.html file.

Usage:
    python add_template.py                         # Interactive mode
    python add_template.py --file data/new_template.json  # From JSON file
"""

import os
import sys
import json
import argparse
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.utils import (
        read_html_file, write_html_file, read_json_file, write_json_file,
        validate_template, print_banner
    )
except ImportError:
    from utils import (
        read_html_file, write_html_file, read_json_file, write_json_file,
        validate_template, print_banner
    )


# Icon options for templates
ICON_OPTIONS = {
    '1': ('fas fa-seedling', 'text-green-500', 'bg-green-50 dark:bg-green-900/20', 'Seedling (Growth/Beginner)'),
    '2': ('fas fa-brain', 'text-purple-500', 'bg-purple-50 dark:bg-purple-900/20', 'Brain (Thinking/Analysis)'),
    '3': ('fas fa-code', 'text-blue-500', 'bg-blue-50 dark:bg-blue-900/20', 'Code (Programming)'),
    '4': ('fas fa-chalkboard-teacher', 'text-orange-500', 'bg-orange-50 dark:bg-orange-900/20', 'Teacher (Education)'),
    '5': ('fas fa-lightbulb', 'text-yellow-500', 'bg-yellow-50 dark:bg-yellow-900/20', 'Lightbulb (Ideas)'),
    '6': ('fas fa-rocket', 'text-red-500', 'bg-red-50 dark:bg-red-900/20', 'Rocket (Launch/Speed)'),
    '7': ('fas fa-puzzle-piece', 'text-indigo-500', 'bg-indigo-50 dark:bg-indigo-900/20', 'Puzzle (Problem Solving)'),
    '8': ('fas fa-book', 'text-teal-500', 'bg-teal-50 dark:bg-teal-900/20', 'Book (Learning)'),
    '9': ('fas fa-flask', 'text-pink-500', 'bg-pink-50 dark:bg-pink-900/20', 'Flask (Experiment)'),
    '10': ('fas fa-robot', 'text-gray-500', 'bg-gray-50 dark:bg-gray-900/20', 'Robot (AI/Automation)'),
}

DIFFICULTY_OPTIONS = ['Beginner', 'Intermediate', 'Advanced', 'All Levels']

CATEGORY_OPTIONS = [
    'Learning Method',
    'Self Testing',
    'Hands-On',
    'Structured Learning',
    'Problem Solving',
    'Creative Writing',
    'Code Review',
    'Research',
    'Interview Prep',
    'Custom'
]


def get_template_from_input():
    """Get template data through interactive input"""
    print("📝 Enter the new template details:\n")
    
    template = {}
    
    # Title
    template['title'] = input("Template Title (e.g., 'Socratic Learning Method'): ").strip()
    
    # Category
    print("\nSelect Category:")
    for i, cat in enumerate(CATEGORY_OPTIONS, 1):
        print(f"   {i}. {cat}")
    cat_choice = input("Enter number or custom category: ").strip()
    
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(CATEGORY_OPTIONS):
        template['category'] = CATEGORY_OPTIONS[int(cat_choice) - 1]
        if template['category'] == 'Custom':
            template['category'] = input("Enter custom category: ").strip()
    else:
        template['category'] = cat_choice
    
    # Icon
    print("\nSelect Icon:")
    for key, (icon, color, bg, desc) in ICON_OPTIONS.items():
        print(f"   {key}. {desc}")
    icon_choice = input("Enter number [1]: ").strip() or '1'
    
    if icon_choice in ICON_OPTIONS:
        template['icon'] = ICON_OPTIONS[icon_choice][0]
        template['iconColor'] = ICON_OPTIONS[icon_choice][1]
        template['bgColor'] = ICON_OPTIONS[icon_choice][2]
    else:
        template['icon'] = 'fas fa-robot'
        template['iconColor'] = 'text-purple-500'
        template['bgColor'] = 'bg-purple-50 dark:bg-purple-900/20'
    
    # Difficulty
    print("\nSelect Difficulty:")
    for i, diff in enumerate(DIFFICULTY_OPTIONS, 1):
        print(f"   {i}. {diff}")
    diff_choice = input("Enter number [2]: ").strip() or '2'
    
    if diff_choice.isdigit() and 1 <= int(diff_choice) <= len(DIFFICULTY_OPTIONS):
        template['difficulty'] = DIFFICULTY_OPTIONS[int(diff_choice) - 1]
    else:
        template['difficulty'] = 'Intermediate'
    
    # Description
    template['description'] = input("\nShort Description (1-2 sentences): ").strip()
    
    # Template Content
    print("\n📄 Enter the prompt template (type 'END' on a new line when finished):")
    print("   TIP: Use **bold** for emphasis, [PLACEHOLDER] for user inputs\n")
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    template['template'] = '\n'.join(lines)
    
    # Example
    template['example'] = input("\nExample usage (e.g., 'Replace [TOPIC] with React Hooks'): ").strip()
    
    # Tips
    template['tips'] = input("Pro tip for using this template: ").strip()
    
    # Estimated time
    template['estimatedTime'] = input("Estimated time (e.g., '30-60 min') [30-60 min]: ").strip() or '30-60 min'
    
    return template


def format_template_js(template):
    """Format template data as JavaScript object string"""
    
    # Escape the template content for JavaScript
    template_content = template['template'].replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    
    js_obj = f'''            {{
                title: "{template['title']}",
                icon: "{template.get('icon', 'fas fa-robot')}",
                iconColor: "{template.get('iconColor', 'text-purple-500')}",
                bgColor: "{template.get('bgColor', 'bg-purple-50 dark:bg-purple-900/20')}",
                category: "{template['category']}",
                difficulty: "{template.get('difficulty', 'Intermediate')}",
                description: "{template['description']}",
                template: `{template_content}`,
                example: "{template['example']}",
                tips: "{template['tips']}",
                estimatedTime: "{template.get('estimatedTime', '30-60 min')}"
            }}'''
    
    return js_obj


def add_template_to_html(html_content, template):
    """Add a new template to the learningTemplates array in HTML"""
    
    # Find the learningTemplates array
    pattern = r'(const\s+learningTemplates\s*=\s*\[)(.*?)(\n\s*\];)'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if not match:
        print("❌ Could not find 'learningTemplates' array in HTML file!")
        return None
    
    # Get the existing content
    array_start = match.group(1)
    array_content = match.group(2)
    array_end = match.group(3)
    
    # Format the new template
    new_template_js = format_template_js(template)
    
    # Add comma after last item if there's existing content
    if array_content.strip():
        if not array_content.rstrip().endswith(','):
            array_content = array_content.rstrip() + ','
        new_array_content = array_content + '\n' + new_template_js
    else:
        new_array_content = '\n' + new_template_js
    
    # Reconstruct the array
    new_array = array_start + new_array_content + array_end
    
    # Replace in HTML
    new_html = html_content[:match.start()] + new_array + html_content[match.end():]
    
    return new_html


def update_template_count(html_content, increment=1):
    """Update the template count in statistics"""
    # Find pattern like: <div class="text-4xl...">4</div> for templates
    pattern = r'(<div class="text-4xl md:text-5xl font-black mb-1">)(\d+)(</div>\s*<div class="text-sm opacity-80">Templates</div>)'
    match = re.search(pattern, html_content)
    
    if match:
        current_count = int(match.group(2))
        new_count = current_count + increment
        new_html = html_content[:match.start()] + match.group(1) + str(new_count) + match.group(3) + html_content[match.end():]
        return new_html
    
    return html_content


def main():
    print_banner("Add New Template")
    
    parser = argparse.ArgumentParser(description='Add a new learning template to AI Karyashala')
    parser.add_argument('--file', '-f', type=str, help='Path to JSON file containing template data')
    parser.add_argument('--html', type=str, default='index.html', help='Path to HTML file (default: index.html)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Use interactive mode')
    
    args = parser.parse_args()
    
    # Determine HTML file path
    html_path = args.html
    if not os.path.exists(html_path):
        html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    
    if not os.path.exists(html_path):
        print(f"❌ HTML file not found: {html_path}")
        print("   Please provide the correct path using --html option")
        sys.exit(1)
    
    print(f"📂 HTML File: {html_path}\n")
    
    # Get template data
    if args.file:
        print(f"📄 Loading template data from: {args.file}\n")
        template = read_json_file(args.file)
        if not template:
            sys.exit(1)
    else:
        template = get_template_from_input()
    
    # Validate template data
    print("\n🔍 Validating template data...")
    if not validate_template(template):
        sys.exit(1)
    print("✅ Template data is valid!\n")
    
    # Show preview
    print("📋 Template Preview:")
    print("-" * 40)
    print(f"   Title: {template['title']}")
    print(f"   Category: {template['category']}")
    print(f"   Difficulty: {template.get('difficulty', 'Intermediate')}")
    print(f"   Time: {template.get('estimatedTime', '30-60 min')}")
    print(f"   Description: {template['description'][:50]}...")
    print("-" * 40)
    
    # Confirm
    confirm = input("\n⚠️  Add this template to the website? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    # Read HTML file
    print("\n📖 Reading HTML file...")
    html_content = read_html_file(html_path)
    if not html_content:
        sys.exit(1)
    
    # Add template
    print("➕ Adding new template...")
    new_html = add_template_to_html(html_content, template)
    if not new_html:
        sys.exit(1)
    
    # Update count
    new_html = update_template_count(new_html)
    
    # Write back
    print("💾 Saving changes...")
    if write_html_file(html_path, new_html):
        print(f"\n✅ SUCCESS! '{template['title']}' has been added to AI Karyashala!")
        print(f"   Open {html_path} in your browser to see the changes.")
    else:
        print("\n❌ Failed to save changes.")
        sys.exit(1)
    
    # Save to backup JSON
    backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'templates_backup.json')
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    existing_templates = read_json_file(backup_path) or []
    existing_templates.append(template)
    write_json_file(backup_path, existing_templates)
    print(f"📦 Template also saved to: {backup_path}")


if __name__ == '__main__':
    main()