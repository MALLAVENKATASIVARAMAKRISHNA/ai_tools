#!/usr/bin/env python3
"""
AI Karyashala - Add New Tool Script
====================================
This script adds a new AI tool to the index.html file.

Usage:
    python add_tool.py                    # Interactive mode
    python add_tool.py --file data/new_tool.json   # From JSON file
    python add_tool.py --interactive      # Interactive mode (explicit)
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
        validate_tool, print_banner
    )
except ImportError:
    from utils import (
        read_html_file, write_html_file, read_json_file, write_json_file,
        validate_tool, print_banner
    )


def get_tool_from_input():
    """Get tool data through interactive input"""
    print("📝 Enter the new tool details:\n")
    
    tool = {}
    
    # Required fields
    tool['name'] = input("Tool Name (e.g., 'Midjourney'): ").strip()
    tool['logo'] = input("Logo URL (image URL or icon class like 'fas fa-robot'): ").strip()
    
    if tool['logo'].startswith('fa'):
        tool['logoType'] = 'icon'
    else:
        tool['logoType'] = 'image'
    
    tool['category'] = input("Category (e.g., 'Image Generation', 'Productivity'): ").strip()
    
    print("\nDescription (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    tool['description'] = ' '.join(lines)
    
    features_input = input("\nFeatures (comma-separated, e.g., 'Text to image, Style transfer, High resolution'): ").strip()
    tool['features'] = [f.strip() for f in features_input.split(',') if f.strip()]
    
    use_cases_input = input("Use Cases (comma-separated, e.g., 'Design, Marketing, Art'): ").strip()
    tool['useCases'] = [u.strip() for u in use_cases_input.split(',') if u.strip()]
    
    tool['pricing'] = input("Pricing (Free/Freemium/Paid) [Freemium]: ").strip() or 'Freemium'
    
    rating_input = input("Rating (1.0-5.0) [4.5]: ").strip()
    tool['rating'] = float(rating_input) if rating_input else 4.5
    
    tool['website'] = input("Website URL: ").strip()
    tool['docs'] = input("Documentation URL: ").strip()
    
    return tool


def format_tool_js(tool):
    """Format tool data as JavaScript object string"""
    features_str = json.dumps(tool['features'])
    use_cases_str = json.dumps(tool.get('useCases', []))
    
    # Escape description for JavaScript
    description = tool['description'].replace('"', '\\"').replace('\n', ' ')
    
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
    
    # Find the aiTools array
    pattern = r'(const\s+aiTools\s*=\s*\[)(.*?)(\n\s*\];)'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if not match:
        print("❌ Could not find 'aiTools' array in HTML file!")
        return None
    
    # Get the existing content
    array_start = match.group(1)
    array_content = match.group(2)
    array_end = match.group(3)
    
    # Format the new tool
    new_tool_js = format_tool_js(tool)
    
    # Add comma after last item if there's existing content
    if array_content.strip():
        # Check if there's already a trailing comma
        if not array_content.rstrip().endswith(','):
            array_content = array_content.rstrip() + ','
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
    # Find and update the tool count
    pattern = r'(<div class="text-4xl md:text-5xl font-black mb-1" id="tool-count">)(\d+)(\+</div>)'
    match = re.search(pattern, html_content)
    
    if match:
        current_count = int(match.group(2))
        new_count = current_count + increment
        new_html = html_content[:match.start()] + match.group(1) + str(new_count) + match.group(3) + html_content[match.end():]
        return new_html
    
    return html_content


def main():
    print_banner("Add New Tool")
    
    parser = argparse.ArgumentParser(description='Add a new AI tool to AI Karyashala')
    parser.add_argument('--file', '-f', type=str, help='Path to JSON file containing tool data')
    parser.add_argument('--html', type=str, default='index.html', help='Path to HTML file (default: index.html)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Use interactive mode')
    
    args = parser.parse_args()
    
    # Determine HTML file path
    html_path = args.html
    if not os.path.exists(html_path):
        # Try parent directory
        html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
    
    if not os.path.exists(html_path):
        print(f"❌ HTML file not found: {html_path}")
        print("   Please provide the correct path using --html option")
        sys.exit(1)
    
    print(f"📂 HTML File: {html_path}\n")
    
    # Get tool data
    if args.file:
        print(f"📄 Loading tool data from: {args.file}\n")
        tool = read_json_file(args.file)
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
    print("-" * 40)
    print(f"   Name: {tool['name']}")
    print(f"   Category: {tool['category']}")
    print(f"   Pricing: {tool.get('pricing', 'Freemium')}")
    print(f"   Rating: {tool.get('rating', 4.5)}")
    print(f"   Features: {', '.join(tool['features'][:3])}...")
    print(f"   Website: {tool['website']}")
    print("-" * 40)
    
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
        print(f"\n✅ SUCCESS! '{tool['name']}' has been added to AI Karyashala!")
        print(f"   Open {html_path} in your browser to see the changes.")
    else:
        print("\n❌ Failed to save changes.")
        sys.exit(1)
    
    # Save to backup JSON
    backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tools_backup.json')
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    existing_tools = read_json_file(backup_path) or []
    existing_tools.append(tool)
    write_json_file(backup_path, existing_tools)
    print(f"📦 Tool also saved to: {backup_path}")


if __name__ == '__main__':
    main()