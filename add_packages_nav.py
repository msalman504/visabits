
import os
import re

def get_relative_path(current_file_path):
    # Count how many folders deep we are from root
    depth = current_file_path.count(os.sep) - 1 # Assuming d:\...\visabits - Copy\index.html is depth 0 relative to root
    # Actually, simpler: check the path of 'about.html' in the file and copy it? 
    # Or just calculate based on file location.
    # Root is where index.html is.
    if current_file_path.endswith('index.html') and os.path.dirname(current_file_path).endswith('visabits - Copy'):
        return "packages.html"
    
    # Calculate depth from root
    # Root dir is roughly determined by presence of 'index.html'
    # But easier: content detection.
    return "packages.html" # Placeholder, will be replaced in logic

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "Packages" in content and 'href="packages.html"' in content:
        print(f"Skipping {file_path} - already has Packages link")
        return

    # Determine relative path prefix
    # Look for about.html link to guess prefix
    about_match = re.search(r'href="([^"]*)about\.html"', content)
    prefix = ""
    if about_match:
        prefix = about_match.group(1)
    
    packages_link = f'{prefix}packages.html'
    
    print(f"Updating {file_path} with link {packages_link}")

    # Desktop Menu Insertion
    # Insert after the closing div of the countries dropdown (Mega Menu)
    # The countries dropdown button has id="desktop-countries-btn"
    # The container is <div class="relative"> ... </div>
    # We look for the closing </div> of that relative container.
    # Pattern: <div class="relative">.*?</div> (non-greedy, including newlines)
    # But regex for nested divs is hard.
    # Alternative strategy: Insert BEFORE <a href=".*about.html"
    
    # Desktop Link HTML
    desktop_link = f'\n                        <a href="{packages_link}"\n                            class="text-slate-600 hover:text-primary font-medium transition-colors hover:bg-slate-50 px-3 py-2 rounded-lg">Packages</a>'

    # Mobile Link HTML
    mobile_link = f'\n                <a href="{packages_link}"\n                    class="block px-3 py-3 rounded-lg text-base font-medium text-slate-600 hover:bg-slate-50 hover:text-primary">Packages</a>'

    # 1. Desktop Update
    # Find the About link in desktop menu
    # It usually looks like: <a href="about.html" ...>About</a>
    # We want to insert BEFORE it.
    
    # Regex for Desktop About Link
    # We need to distinguish between desktop and mobile about link.
    # Desktop one is usually inside <div class="ml-10 flex items-baseline space-x-8"> ... </div>
    # Or just replace the first occurrence of <a href="...about.html" if we are careful?
    # No, mobile one comes later.
    
    # Better anchor: The Countries Dropdown.
    # It ends with </div>.
    # And then followed by About link.
    # Let's search for the About link that follows the countries dropdown.
    
    # Pattern: </div>\s*<a href="[^"]*about\.html"
    desktop_pattern = r'(</div>\s*)(<a href="[^"]*about\.html"[^>]*>About</a>)'
    
    # Check if we find it
    if re.search(desktop_pattern, content):
        content = re.sub(desktop_pattern, f'\\1{desktop_link}\\2', content, count=1)
    else:
        print(f"Warning: Could not find insertion point for Desktop menu in {file_path}")

    # 2. Mobile Update
    # Find the Mobile About Link
    # It's inside <div id="mobile-menu"> ... </div>
    # It usually comes after the countries accordions.
    # Pattern: <a href="[^"]*about\.html"[^>]*class="[^"]*block[^"]*"[^>]*>About</a>
    # We need to be specific to avoid matching the desktop one again if regex was loose.
    # The mobile link has 'block' class usually.
    
    mobile_pattern = r'(<a href="[^"]*about\.html"[^>]*class="[^"]*block[^"]*"[^>]*>About</a>)'
    
    # Use a different strategy for mobile if possible, but 'block' class is a good differentiator
    # The desktop one has 'inline-block' or just 'text-slate-600 ... px-3 py-2'
    
    if re.search(mobile_pattern, content):
        # We want to insert BEFORE the mobile About link
        # But wait, in the file content, the mobile about link is the SECOND occurrence of an About link?
        # Usually yes.
        pass
    
    # Let's try to match the specific context of mobile menu items
    # They are siblings.
    
    # We can use findall to see matches, and replace the one that looks like mobile.
    matches = list(re.finditer(mobile_pattern, content))
    if matches:
        # Usually successful. replace the last one? or all?
        # There should be only one in the mobile menu section.
        # But wait, index.html might have multiple? No.
        
        # Let's replace the one that matches perfectly.
        content = re.sub(mobile_pattern, f'{mobile_link}\\1', content) # Insert before
    else:
        print(f"Warning: Could not find insertion point for Mobile menu in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root_dir = os.getcwd() # Should be d:\1\agents\visabits - Copy
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html") and file != "packages.html": # Skip packages.html as it is source of truth/already good (mostly)
                # But wait, packages.html might need untangling if links are wrong? No, I saw them they are fine.
                file_path = os.path.join(root, file)
                try:
                    update_file(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
