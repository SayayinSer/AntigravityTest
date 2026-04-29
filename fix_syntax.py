import os
import re

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix |length
    content = re.sub(r'<\?php if \((.*?)\|length(.*?)\): \?>', r'<?php if (count(\1 ?? []) \2): ?>', content)
    
    # Fix python 'in' to in_array
    content = re.sub(r'<\?php if \((.*?)\s+in\s+(.*?)\): \?>', r'<?php if (in_array(\1, \2 ?? [])): ?>', content)
    
    # Fix python formatters like "{:,}".format(val) or val|format
    content = re.sub(r'<\?= htmlspecialchars\(strval\(\$(.*?) \/\* filter \*\/ format\([\'"](.*?)[\'"]\)(.*?)\)\) \?>', r'<?= number_format((float)($\1 ?? 0), 2) ?>', content)
    
    # Fallback fixes for common python idioms remaining
    content = content.replace('.length', '')
    content = re.sub(r'<\?php if \(\$(.*?) \/\* filter \*\/ length(.*?)\): \?>', r'<?php if (count($\1 ?? []) \2): ?>', content)

    # General brute-force cleanup for testing (turn off syntax checking for known python loops if they broke)
    content = content.replace('is_closed', '$is_closed')
    
    # Just fix the specific lines
    content = re.sub(r'\$(.*?) \/\* filter \*\/ length', r'count($\1 ?? [])', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                fix_file(os.path.join(root, file))
    print("Syntax fix applied.")
