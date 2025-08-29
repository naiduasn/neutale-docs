#!/usr/bin/env python3
"""
Fix API Specification Issues
- Fix compact mapping errors (default: en -> default: "en")
- Remove duplicate path definitions
"""

import re
import sys

def fix_api_spec(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Quote default values for YAML compliance
    print("Fixing compact mapping issues...")
    content = re.sub(r'(\s+)default: en(\s)', r'\1default: "en"\2', content)
    content = re.sub(r'(\s+)default: published(\s)', r'\1default: "published"\2', content)
    
    # Fix 2: Find and remove duplicate sections
    print("Looking for duplicate sections...")
    lines = content.split('\n')
    
    # Find billing plans duplicates
    billing_indices = []
    webhook_indices = []
    
    for i, line in enumerate(lines):
        if '/api/billing/plans:' in line.strip():
            billing_indices.append(i)
        elif '/api/webhooks/dodo:' in line.strip():
            webhook_indices.append(i)
    
    print(f"Found billing plans at lines: {[i+1 for i in billing_indices]}")
    print(f"Found webhook dodo at lines: {[i+1 for i in webhook_indices]}")
    
    # Remove duplicates - keep first occurrence, remove others
    lines_to_remove = set()
    
    # For each duplicate billing section
    if len(billing_indices) > 1:
        print(f"Removing duplicate billing sections...")
        for i in range(1, len(billing_indices)):
            start_idx = billing_indices[i]
            # Find the end of this section by looking for next major section
            end_idx = len(lines)
            for j in range(start_idx + 1, len(lines)):
                line = lines[j].strip()
                if line.startswith('# ') or (line.startswith('/api/') and not line.startswith('/api/billing')):
                    end_idx = j
                    break
            
            print(f"Marking lines {start_idx+1} to {end_idx} for removal")
            lines_to_remove.update(range(start_idx, end_idx))
    
    # For duplicate webhook sections
    if len(webhook_indices) > 1:
        print(f"Removing duplicate webhook sections...")
        for i in range(1, len(webhook_indices)):
            start_idx = webhook_indices[i]
            # Find end of webhook section
            end_idx = len(lines)
            for j in range(start_idx + 1, len(lines)):
                line = lines[j].strip()
                if line.startswith('# ') and 'Webhook' not in line:
                    end_idx = j
                    break
            
            print(f"Marking webhook lines {start_idx+1} to {end_idx} for removal")
            lines_to_remove.update(range(start_idx, end_idx))
    
    # Remove marked lines
    if lines_to_remove:
        print(f"Removing {len(lines_to_remove)} duplicate lines...")
        cleaned_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
        content = '\n'.join(cleaned_lines)
    
    # Write back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("API specification fixed!")

if __name__ == "__main__":
    fix_api_spec('api-spec.yaml')