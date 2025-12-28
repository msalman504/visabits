
import os
import re

def update_phone_numbers(root_dir):
    # Old number patterns
    # 1. Plain digits (for hrefs): 447412855412
    # 2. Display format (with possible spaces/newlines): +44 7412 855412
    
    # New number
    new_digits = "923144152590"
    new_display = "+92 314 415 2590"
    
    # Regex for display: matches +44 then optional whitespace then 7412 then optional whitespace then 855412
    regex_display = re.compile(r'\+44\s*7412\s*855412')
    
    # Regex for links which might look like wa.me/447412855412 or tel:+447412855412
    # We can just replace the digit sequence 447412855412
    regex_digits = re.compile(r'447412855412')

    files_updated = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    
                    # Replace display first (the more specific pattern)
                    # We might want to be careful not to double replace if logic overlaps, 
                    # but here the patterns are distinct enough (+44 vs 4474...)
                    
                    # Actually, for display, let's look for the visual one
                    if regex_display.search(new_content):
                        new_content = regex_display.sub(new_display, new_content)
                    
                    # Replace links/digits
                    if regex_digits.search(new_content):
                        new_content = regex_digits.sub(new_digits, new_content)
                        
                    if new_content != content:
                        print(f"Updating {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        files_updated += 1
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

    print(f"Total files updated: {files_updated}")

if __name__ == "__main__":
    # Current directory
    root_dir = "."
    update_phone_numbers(root_dir)
