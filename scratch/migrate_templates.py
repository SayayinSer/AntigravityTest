import os
import re

SRC_DIR = "d:\\aaProyectos\\Entorno01\\app\\templates"
DST_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

def process_file(content):
    # Reemplazar {{ var }} por <?= htmlspecialchars($var ?? '') ?>
    content = re.sub(r'\{\{\s*(.*?)\s*\}\}', r'<?= htmlspecialchars(strval($\1 ?? "")) ?>', content)
    # Arreglar variables con atributos (ej: user.username -> user->username)
    # Nota: esto es ingenuo y se afinará en PHP, pero ayuda enormemente
    def fix_var(match):
        code = match.group(0)
        code = code.replace('.', '->')
        # Reemplazar llamadas a funciones basicas de Jinja
        code = code.replace('|', ' /* filter */ ')
        return code
    
    content = re.sub(r'<\?=\s+htmlspecialchars\(.*?\)\s+\?>', fix_var, content)
    
    # Reemplazar {% if condition %}
    content = re.sub(r'\{%\s*if\s+(.*?)\s*%\}', r'<?php if (\1): ?>', content)
    content = re.sub(r'\{%\s*elif\s+(.*?)\s*%\}', r'<?php elseif (\1): ?>', content)
    content = re.sub(r'\{%\s*else\s*%\}', r'<?php else: ?>', content)
    content = re.sub(r'\{%\s*endif\s*%\}', r'<?php endif; ?>', content)
    
    # Reemplazar {% for item in list %}
    content = re.sub(r'\{%\s*for\s+(\w+)\s+in\s+(.*?)\s*%\}', r'<?php foreach ($\2 ?? [] as $\1): ?>', content)
    content = re.sub(r'\{%\s*endfor\s*%\}', r'<?php endforeach; ?>', content)
    
    # Fix python 'not' to PHP '!'
    content = content.replace('<?php if (not $', '<?php if (!$')
    
    # URLfor url_for
    content = re.sub(r'url_for\([\'"](.*?)[\'"]\)', r'"/NucleoTallerV1/\1"', content)

    return content

def migrate():
    if not os.path.exists(DST_DIR):
        os.makedirs(DST_DIR)
        
    for root, dirs, files in os.walk(SRC_DIR):
        rel_path = os.path.relpath(root, SRC_DIR)
        dst_root = os.path.join(DST_DIR, rel_path)
        if not os.path.exists(dst_root):
            os.makedirs(dst_root)
            
        for file in files:
            if file.endswith('.html'):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, file.replace('.html', '.view.php'))
                
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                new_content = process_file(content)
                
                with open(dst_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Migrated: {src_file} -> {dst_file}")

if __name__ == '__main__':
    migrate()
