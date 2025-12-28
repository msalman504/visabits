import glob
import re

# Define the target links
LINKEDIN_URL = "https://www.linkedin.com/company/visa-bits/"
FACEBOOK_URL = "https://www.facebook.com/profile.php?id=61575915765867"
INSTAGRAM_URL = "https://www.instagram.com/visabits/"

# Regex patterns to find the placeholder links
# We look for the <a> tag containing the specific icon class
# Note: The order in the HTML is LinkedIn, Facebook, Instagram

# Pattern for LinkedIn
# <a href="#" class="text-slate-400 hover:text-accent transition-colors"><i class="fab fa-linkedin text-xl"></i></a>
linkedin_pattern = r'<a href="#" class="([^"]+)"><i\s+class="fab fa-linkedin text-xl"></i></a>'
linkedin_replacement = f'<a href="{LINKEDIN_URL}" class="\\1" target="_blank" rel="noopener noreferrer"><i class="fab fa-linkedin text-xl"></i></a>'

# Pattern for Facebook
# <a href="#" class="text-slate-400 hover:text-accent transition-colors"><i class="fab fa-facebook text-xl"></i></a>
facebook_pattern = r'<a href="#" class="([^"]+)"><i\s+class="fab fa-facebook text-xl"></i></a>'
facebook_replacement = f'<a href="{FACEBOOK_URL}" class="\\1" target="_blank" rel="noopener noreferrer"><i class="fab fa-facebook text-xl"></i></a>'

# Pattern for Instagram
# <a href="#" class="text-slate-400 hover:text-accent transition-colors"><i class="fab fa-instagram text-xl"></i></a>
instagram_pattern = r'<a href="#" class="([^"]+)"><i\s+class="fab fa-instagram text-xl"></i></a>'
instagram_replacement = f'<a href="{INSTAGRAM_URL}" class="\\1" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram text-xl"></i></a>'

# Find all HTML files
files = glob.glob('**/*.html', recursive=True)

for file_path in files:
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply replacements
    content = re.sub(linkedin_pattern, linkedin_replacement, content)
    content = re.sub(facebook_pattern, facebook_replacement, content)
    content = re.sub(instagram_pattern, instagram_replacement, content)
    
    if content != original_content:
        print(f"  - Updated links in {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"  - No changes needed or pattern not found in {file_path}")

print("Done.")
