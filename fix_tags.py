import os

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

def fix_html_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix mangled tags
    content = content.replace('<$p', '<p')
    content = content.replace('</$p', '</p')
    content = content.replace('<$div', '<div')
    content = content.replace('</$div', '</div>')
    content = content.replace('<$span', '<span')
    content = content.replace('</$span', '</span>')
    content = content.replace('<$table', '<table')
    content = content.replace('</$table', '</table>')
    content = content.replace('<$tr', '<tr')
    content = content.replace('</$tr', '</tr>')
    content = content.replace('<$td', '<td')
    content = content.replace('</$td', '</td>')
    content = content.replace('<$th', '<th')
    content = content.replace('</$th', '</th>')
    content = content.replace('<$h', '<h')
    content = content.replace('</$h', '</h')
    
    # Also fix residual double $$
    content = content.replace('$$', '$')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                fix_html_tags(os.path.join(root, file))
    print("HTML Tags Fixed.")
