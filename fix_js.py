import os
import re

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

def fix_js_blocks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <script> ... </script> blocks
    def fix_js(match):
        script_content = match.group(0)
        # Change ? (condition) { to if (condition) { inside script
        fixed_content = re.sub(r'\?\s*\((.*?)\)\s*\{', r'if (\1) {', script_content)
        return fixed_content

    new_content = re.sub(r'<script.*?>.*?</script>', fix_js, content, flags=re.DOTALL)
    
    # Also fix some other mangled things
    new_content = new_content.replace('border-$t', 'border-t')
    new_content = new_content.replace('$p-10', 'p-10')
    new_content = new_content.replace('$p-8', 'p-8')
    new_content = new_content.replace('$p-4', 'p-4')
    new_content = new_content.replace('$p-6', 'p-6')
    new_content = new_content.replace('$p-0', 'p-0')
    new_content = new_content.replace('$p-5', 'p-5')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                fix_js_blocks(os.path.join(root, file))
    print("JS Blocks and Utility Classes Fixed.")
