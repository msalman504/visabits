
import os
import re

def update_privacy_links(root_dir):
    privacy_filename = "privacy-policy.html"
    
    # Regex to find the privacy policy list item
    # Pattern 1: href then class
    regex_1 = r'(<li>\s*<a\s+href=["\'](?:#|[^"\']*)["\']\s+class=["\']([^"\']*)["\']\s*>\s*Privacy\s+Policy\s*</a>\s*</li>)'
    # Pattern 2: class then href
    regex_2 = r'(<li>\s*<a\s+class=["\']([^"\']*)["\']\s+href=["\'](?:#|[^"\']*)["\']\s*>\s*Privacy\s+Policy\s*</a>\s*</li>)'
    
    patterns = [regex_1, regex_2]
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                # Skip the privacy policy file itself to avoid self-referencing if not needed (though it's fine)
                # But we should ensure the link in privacy-policy.html is also correct (it might be absolute or relative)
                
                # Calculate relative path to privacy-policy.html
                # If we are in d:\1\agents\visabits - Copy\countries\uk\tourist.html
                # And privacy is in d:\1\agents\visabits - Copy\privacy-policy.html
                # Relpath is ..\..\privacy-policy.html
                
                try:
                    rel_path = os.path.relpath(os.path.join(root_dir, privacy_filename), root)
                    # Convert Windows backslashes to forward slashes for HTML
                    rel_path = rel_path.replace(os.sep, '/')
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Function to replace the href in the matched string
                    new_content = content
                    for pattern in patterns:
                         def replacement_func(match):
                            full_match = match.group(1)
                            # Group 2 captures the class content in both regexes now?
                            # Regex 1: group(2) is class. Regex 2: group(2) is class.
                            classes = match.group(2)
                            
                            if file == privacy_filename:
                                 return f'<li><a href="{privacy_filename}" class="{classes}">Privacy Policy</a></li>'
                            
                            return f'<li><a href="{rel_path}" class="{classes}">Privacy Policy</a></li>'

                         new_content = re.sub(pattern, replacement_func, new_content, flags=re.IGNORECASE)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file_path} -> href='{rel_path}'")
                    else:
                        print(f"No match found or already updated: {file_path}")
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    root_directory = r"d:\1\agents\visabits - Copy"
    update_privacy_links(root_directory)
