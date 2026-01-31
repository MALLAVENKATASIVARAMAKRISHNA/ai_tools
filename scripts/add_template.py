#!/usr/bin/env python3
"""
AI Karyashala - Add New Template Script (Standalone)
=====================================================
Usage:
    python3 add_template.py                                  # Interactive mode
    python3 add_template.py --file ../data/new_template.json # From JSON file
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime


# ============================================
# UTILITY FUNCTIONS (Built-in)
# ============================================

def read_html_file(filepath):
    """Read the HTML file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found!")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def write_html_file(filepath, content):
    """Write content to HTML file with backup"""
    try:
        if os.path.exists(filepath):
            backup_dir = os.path.join(os.path.dirname(filepath), 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_name = f'index_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            backup_path = os.path.join(backup_dir, backup_name)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            print(f"📦 Backup created: {backup_path}")
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False


def read_json_file(filepath):
    """Read JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return None


def write_json_file(filepath, data):
    """Write data to JSON file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error writing JSON: {e}")
        return False


def validate_template(template_data):
    """Validate template data structure"""
    required_fields = ['title', 'category', 'description', 'template', 'example', 'tips']
    missing = [field for field in required_fields if field not in template_data]
    
    if missing:
        print(f"❌ Missing required fields: {', '.join(missing)}")
        return False
    
    # Set defaults for optional fields
    defaults = {
        'icon': 'fas fa-robot',
        'iconColor': 'text-purple-500',
        'bgColor': 'bg-purple-50 dark:bg-purple-900/20',
        'difficulty': 'Intermediate',
        'estimatedTime': '30-60 min'
    }
    
    for key, value in defaults.items():
        if key not in template_data:
            template_data[key] = value
    
    return True


def print_banner(title):
    """Print a nice banner"""
    print("\n" + "=" * 60)
    print(f"  🤖 AI Karyashala - {title}")
    print("=" * 60 + "\n")


# ============================================
# ICON OPTIONS
# ============================================

ICON_OPTIONS = {
    '1': ('fas fa-seedling', 'text-green-500', 'bg-green-50 dark:bg-green-900/20', '🌱 Seedling (Beginner)'),
    '2': ('fas fa-brain', 'text-purple-500', 'bg-purple-50 dark:bg-purple-900/20', '🧠 Brain (Thinking)'),
    '3': ('fas fa-code', 'text-blue-500', 'bg-blue-50 dark:bg-blue-900/20', '💻 Code (Programming)'),
    '4': ('fas fa-chalkboard-teacher', 'text-orange-500', 'bg-orange-50 dark:bg-orange-900/20', '👨‍🏫 Teacher'),
    '5': ('fas fa-lightbulb', 'text-yellow-500', 'bg-yellow-50 dark:bg-yellow-900/20', '💡 Lightbulb (Ideas)'),
    '6': ('fas fa-rocket', 'text-red-500', 'bg-red-50 dark:bg-red-900/20', '🚀 Rocket (Speed)'),
    '7': ('fas fa-puzzle-piece', 'text-indigo-500', 'bg-indigo-50 dark:bg-indigo-900/20', '🧩 Puzzle'),
    '8': ('fas fa-book', 'text-teal-500', 'bg-teal-50 dark:bg-teal-900/20', '📚 Book (Learning)'),
    '9': ('fas fa-flask', 'text-pink-500', 'bg-pink-50 dark:bg-pink-900/20', '🧪 Flask (Experiment)'),
    '10': ('fas fa-robot', 'text-gray-500', 'bg-gray-50 dark:bg-gray-900/20', '🤖 Robot (AI)'),
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
]


# ============================================
# MAIN FUNCTIONS
# ============================================

def get_template_from_input():
    """Get template data through interactive input"""
    print("📝 Enter the new template details:\n")
    
    template = {}
    
    # Title
    template['title'] = input("Template Title (e.g., 'Socratic Learning'): ").strip()
    
    if not template['title']:
        print("❌ Title cannot be empty!")
        sys.exit(1)
    
    # Category
    print("\nSelect Category:")
    for i, cat in enumerate(CATEGORY_OPTIONS, 1):
        print(f"   {i}. {cat}")
    print(f"   {len(CATEGORY_OPTIONS)+1}. Custom...")
    
    cat_choice = input(f"Enter number (1-{len(CATEGORY_OPTIONS)+1}) [1]: ").strip() or '1'
    
    try:
        cat_index = int(cat_choice) - 1
        if 0 <= cat_index < len(CATEGORY_OPTIONS):
            template['category'] = CATEGORY_OPTIONS[cat_index]
        else:
            template['category'] = input("Enter custom category: ").strip()
    except ValueError:
        template['category'] = cat_choice
    
    # Icon
    print("\nSelect Icon:")
    for key, (icon, color, bg, desc) in ICON_OPTIONS.items():
        print(f"   {key}. {desc}")
    
    icon_choice = input("Enter number [2]: ").strip() or '2'
    
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
    
    try:
        diff_index = int(diff_choice) - 1
        if 0 <= diff_index < len(DIFFICULTY_OPTIONS):
            template['difficulty'] = DIFFICULTY_OPTIONS[diff_index]
        else:
            template['difficulty'] = 'Intermediate'
    except ValueError:
        template['difficulty'] = 'Intermediate'
    
    # Description
    template['description'] = input("\nShort Description (1-2 sentences): ").strip()
    
    # Template Content
    print("\n📄 Enter the prompt template:")
    print("   (Type on multiple lines, then type 'END' on a new line when done)\n")
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    template['template'] = '\n'.join(lines)
    
    # Example
    template['example'] = input("\nExample usage: ").strip()
    
    # Tips
    template['tips'] = input("Pro tip: ").strip()
    
    # Estimated time
    template['estimatedTime'] = input("Estimated time (e.g., '30-60 min') [30-60 min]: ").strip() or '30-60 min'
    
    return template


def format_template_js(template):
    """Format template data as JavaScript object string"""
    
    # Escape the template content for JavaScript backticks
    template_content = template['template']
    template_content = template_content.replace('\\', '\\\\')
    template_content = template_content.replace('`', '\\`')
    template_content = template_content.replace('${', '\\${')
    
    # Escape other strings
    description = template['description'].replace('"', '\\"')
    example = template['example'].replace('"', '\\"')
    tips = template['tips'].replace('"', '\\"')
    
    js_obj = f'''            {{
                title: "{template['title']}",
                icon: "{template.get('icon', 'fas fa-robot')}",
                iconColor: "{template.get('iconColor', 'text-purple-500')}",
                bgColor: "{template.get('bgColor', 'bg-purple-50 dark:bg-purple-900/20')}",
                category: "{template['category']}",
                difficulty: "{template.get('difficulty', 'Intermediate')}",
                description: "{description}",
                template: `{template_content}`,
                example: "{example}",
                tips: "{tips}",
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
        print("   Make sure your HTML has: const learningTemplates = [...]")
        return None
    
    # Get the existing content
    array_start = match.group(1)
    array_content = match.group(2)
    array_end = match.group(3)
    
    # Format the new template
    new_template_js = format_template_js(template)
    
    # Add comma after last item if there's existing content
    if array_content.strip():
        array_content = array_content.rstrip()
        if not array_content.endswith(','):
            array_content = array_content + ','
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
    # Pattern for template count
    pattern = r'(<div class="text-4xl md:text-5xl font-black mb-1">)(\d+)(</div>\s*<div class="text-sm opacity-80">Templates</div>)'
    match = re.search(pattern, html_content)
    
    if match:
        current_count = int(match.group(2))
        new_count = current_count + increment
        new_html = (html_content[:match.start()] + 
                   match.group(1) + str(new_count) + match.group(3) + 
                   html_content[match.end():])
        print(f"📊 Updated template count: {current_count} → {new_count}")
        return new_html
    
    return html_content


def find_html_file():
    """Try to find the index.html file"""
    possible_paths = [
        'index.html',
        '../index.html',
        '../../index.html',
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None


# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    print_banner("Add New Template")
    
    parser = argparse.ArgumentParser(description='Add a new learning template to AI Karyashala')
    parser.add_argument('--file', '-f', type=str, help='Path to JSON file containing template data')
    parser.add_argument('--html', type=str, help='Path to HTML file')
    
    args = parser.parse_args()
    
    # Find HTML file
    if args.html:
        html_path = args.html
    else:
        html_path = find_html_file()
    
    if not html_path or not os.path.exists(html_path):
        print("❌ Could not find index.html!")
        print("   Please specify the path using: --html /path/to/index.html")
        sys.exit(1)
    
    print(f"📂 HTML File: {html_path}\n")
    
    # Get template data
    if args.file:
        json_path = args.file
        if not os.path.isabs(json_path):
            json_path = os.path.abspath(json_path)
        
        print(f"📄 Loading template data from: {json_path}\n")
        template = read_json_file(json_path)
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
    print("-" * 50)
    print(f"   Title:       {template['title']}")
    print(f"   Category:    {template['category']}")
    print(f"   Difficulty:  {template.get('difficulty', 'Intermediate')}")
    print(f"   Time:        {template.get('estimatedTime', '30-60 min')}")
    print(f"   Description: {template['description'][:50]}...")
    print("-" * 50)
    
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
    
    # Check if template already exists
    if f'title: "{template["title"]}"' in html_content:
        print(f"⚠️  Warning: A template named '{template['title']}' may already exist!")
        proceed = input("   Continue anyway? (yes/no): ").strip().lower()
        if proceed not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            sys.exit(0)
    
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
        print(f"\n{'='*50}")
        print(f"✅ SUCCESS! '{template['title']}' has been added!")
        print(f"{'='*50}")
        print(f"\n🌐 Open in browser: file://{html_path}")
    else:
        print("\n❌ Failed to save changes.")
        sys.exit(1)
    
    # Save to backup JSON
    backup_dir = os.path.join(os.path.dirname(html_path), 'data')
    backup_path = os.path.join(backup_dir, 'templates_backup.json')
    
    existing_templates = read_json_file(backup_path) or []
    existing_templates.append(template)
    
    if write_json_file(backup_path, existing_templates):
        print(f"📦 Template backup saved to: {backup_path}")


if __name__ == '__main__':
    main()