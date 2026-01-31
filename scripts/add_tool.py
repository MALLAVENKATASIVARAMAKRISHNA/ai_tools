#!/usr/bin/env python3
"""
AI Karyashala - Add New Tool Script (Standalone)
=================================================
Usage:
    python3 add_tool.py                              # Interactive mode
    python3 add_tool.py --file ../data/new_tool.json # From JSON file
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
        # Create backup first
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


def validate_tool(tool_data):
    """Validate tool data structure"""
    required_fields = ['name', 'logo', 'category', 'description', 'features', 'website', 'docs']
    missing = [field for field in required_fields if field not in tool_data]
    
    if missing:
        print(f"❌ Missing required fields: {', '.join(missing)}")
        return False
    
    # Set defaults for optional fields
    defaults = {
        'logoType': 'image',
        'useCases': [],
        'pricing': 'Freemium',
        'rating': 4.5
    }
    
    for key, value in defaults.items():
        if key not in tool_data:
            tool_data[key] = value
    
    # Auto-detect logoType
    if tool_data['logo'].startswith('fa'):
        tool_data['logoType'] = 'icon'
    
    return True


def print_banner(title):
    """Print a nice banner"""
    print("\n" + "=" * 60)
    print(f"  🤖 AI Karyashala - {title}")
    print("=" * 60 + "\n")


# ============================================
# MAIN FUNCTIONS
# ============================================

def get_tool_from_input():
    """Get tool data through interactive input"""
    print("📝 Enter the new tool details:\n")
    
    tool = {}
    
    # Required fields
    tool['name'] = input("Tool Name (e.g., 'Midjourney'): ").strip()
    
    if not tool['name']:
        print("❌ Tool name cannot be empty!")
        sys.exit(1)
    
    tool['logo'] = input("Logo URL (image URL or 'fas fa-icon'): ").strip()
    
    if tool['logo'].startswith('fa'):
        tool['logoType'] = 'icon'
    else:
        tool['logoType'] = 'image'
    
    tool['category'] = input("Category (e.g., 'Image Generation'): ").strip()
    
    print("\nDescription (one line):")
    tool['description'] = input().strip()
    
    features_input = input("\nFeatures (comma-separated): ").strip()
    tool['features'] = [f.strip() for f in features_input.split(',') if f.strip()]
    
    use_cases_input = input("Use Cases (comma-separated, or press Enter to skip): ").strip()
    if use_cases_input:
        tool['useCases'] = [u.strip() for u in use_cases_input.split(',') if u.strip()]
    else:
        tool['useCases'] = []
    
    print("\nPricing options: 1) Free  2) Freemium  3) Paid")
    pricing_choice = input("Select (1/2/3) [2]: ").strip() or '2'
    pricing_map = {'1': 'Free', '2': 'Freemium', '3': 'Paid'}
    tool['pricing'] = pricing_map.get(pricing_choice, 'Freemium')
    
    rating_input = input("Rating (1.0-5.0) [4.5]: ").strip()
    try:
        tool['rating'] = float(rating_input) if rating_input else 4.5
        tool['rating'] = max(1.0, min(5.0, tool['rating']))  # Clamp between 1-5
    except ValueError:
        tool['rating'] = 4.5
    
    tool['website'] = input("Website URL: ").strip()
    tool['docs'] = input("Documentation URL: ").strip()
    
    return tool


def format_tool_js(tool):
    """Format tool data as JavaScript object string"""
    features_str = json.dumps(tool['features'], ensure_ascii=False)
    use_cases_str = json.dumps(tool.get('useCases', []), ensure_ascii=False)
    
    # Escape description for JavaScript
    description = tool['description'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    
    js_obj = f'''            {{
                name: "{tool['name']}",
                logo: "{tool['logo']}",
                logoType: "{tool.get('logoType', 'image')}",
                category: "{tool['category']}",
                description: "{description}",
                features: {features_str},
                useCases: {use_cases_str},
                pricing: "{tool.get('pricing', 'Freemium')}",
                rating: {tool.get('rating', 4.5)},
                website: "{tool['website']}",
                docs: "{tool['docs']}"
            }}'''
    
    return js_obj


def add_tool_to_html(html_content, tool):
    """Add a new tool to the aiTools array in HTML"""
    
    # Find the aiTools array using regex
    pattern = r'(const\s+aiTools\s*=\s*\[)(.*?)(\n\s*\];)'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if not match:
        print("❌ Could not find 'aiTools' array in HTML file!")
        print("   Make sure your HTML has: const aiTools = [...]")
        return None
    
    # Get the existing content
    array_start = match.group(1)
    array_content = match.group(2)
    array_end = match.group(3)
    
    # Format the new tool
    new_tool_js = format_tool_js(tool)
    
    # Add comma after last item if there's existing content
    if array_content.strip():
        # Remove trailing whitespace and ensure comma
        array_content = array_content.rstrip()
        if not array_content.endswith(','):
            array_content = array_content + ','
        new_array_content = array_content + '\n' + new_tool_js
    else:
        new_array_content = '\n' + new_tool_js
    
    # Reconstruct the array
    new_array = array_start + new_array_content + array_end
    
    # Replace in HTML
    new_html = html_content[:match.start()] + new_array + html_content[match.end():]
    
    return new_html


def update_tool_count(html_content, increment=1):
    """Update the tool count in statistics"""
    pattern = r'(<div class="text-4xl md:text-5xl font-black mb-1" id="tool-count">)(\d+)(\+</div>)'
    match = re.search(pattern, html_content)
    
    if match:
        current_count = int(match.group(2))
        new_count = current_count + increment
        new_html = (html_content[:match.start()] + 
                   match.group(1) + str(new_count) + match.group(3) + 
                   html_content[match.end():])
        print(f"📊 Updated tool count: {current_count} → {new_count}")
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
    print_banner("Add New Tool")
    
    parser = argparse.ArgumentParser(description='Add a new AI tool to AI Karyashala')
    parser.add_argument('--file', '-f', type=str, help='Path to JSON file containing tool data')
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
    
    # Get tool data
    if args.file:
        json_path = args.file
        if not os.path.isabs(json_path):
            json_path = os.path.abspath(json_path)
        
        print(f"📄 Loading tool data from: {json_path}\n")
        tool = read_json_file(json_path)
        if not tool:
            sys.exit(1)
    else:
        tool = get_tool_from_input()
    
    # Validate tool data
    print("\n🔍 Validating tool data...")
    if not validate_tool(tool):
        sys.exit(1)
    print("✅ Tool data is valid!\n")
    
    # Show preview
    print("📋 Tool Preview:")
    print("-" * 50)
    print(f"   Name:        {tool['name']}")
    print(f"   Category:    {tool['category']}")
    print(f"   Pricing:     {tool.get('pricing', 'Freemium')}")
    print(f"   Rating:      {tool.get('rating', 4.5)} ⭐")
    print(f"   Features:    {', '.join(tool['features'][:3])}" + ("..." if len(tool['features']) > 3 else ""))
    print(f"   Website:     {tool['website']}")
    print("-" * 50)
    
    # Confirm
    confirm = input("\n⚠️  Add this tool to the website? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    # Read HTML file
    print("\n📖 Reading HTML file...")
    html_content = read_html_file(html_path)
    if not html_content:
        sys.exit(1)
    
    # Check if tool already exists
    if f'name: "{tool["name"]}"' in html_content:
        print(f"⚠️  Warning: A tool named '{tool['name']}' may already exist!")
        proceed = input("   Continue anyway? (yes/no): ").strip().lower()
        if proceed not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            sys.exit(0)
    
    # Add tool
    print("➕ Adding new tool...")
    new_html = add_tool_to_html(html_content, tool)
    if not new_html:
        sys.exit(1)
    
    # Update count
    new_html = update_tool_count(new_html)
    
    # Write back
    print("💾 Saving changes...")
    if write_html_file(html_path, new_html):
        print(f"\n{'='*50}")
        print(f"✅ SUCCESS! '{tool['name']}' has been added!")
        print(f"{'='*50}")
        print(f"\n🌐 Open in browser: file://{html_path}")
    else:
        print("\n❌ Failed to save changes.")
        sys.exit(1)
    
    # Save to backup JSON
    backup_dir = os.path.join(os.path.dirname(html_path), 'data')
    backup_path = os.path.join(backup_dir, 'tools_backup.json')
    
    existing_tools = read_json_file(backup_path) or []
    existing_tools.append(tool)
    
    if write_json_file(backup_path, existing_tools):
        print(f"📦 Tool backup saved to: {backup_path}")


if __name__ == '__main__':
    main()