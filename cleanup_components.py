import os
import re

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

def cleanup_components_and_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove header/footer if it's a component or modal
    if 'components' in filepath or 'modal' in filepath:
        content = content.replace("<?php include BASE_PATH . 'src/Views/layout/header.php'; ?>\n", "")
        content = content.replace("\n<?php include BASE_PATH . 'src/Views/layout/footer.php'; ?>", "")

    # 2. Fix Alpine.js / JS mangled variables
    # $el->remove() -> $el.remove()
    # $dispatch-> -> $dispatch.
    # $refs-> -> $refs.
    content = content.replace('$el->', '$el.')
    content = content.replace('$dispatch->', '$dispatch.')
    content = content.replace('$refs->', '$refs.')
    
    # 3. Fix HTMX mangled paths
    content = content.replace('/$order/', '/order/')
    content = content.replace('/$vehicles', '/vehicles')
    content = content.replace('/$clients', '/clients')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                cleanup_components_and_js(os.path.join(root, file))
    print("Component and JS Cleanup Applied.")
