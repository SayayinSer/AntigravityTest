import os

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

replacements = {
    'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
    'Ã±': 'ñ', 'Ã‘': 'Ñ', 'Ã¡': 'á', 'Ã‰': 'É', 'Ã“': 'Ó', 
    'Ãš': 'Ú', 'Â¿': '¿', 'Â¡': '¡', 'Ã ': 'à', 'Ã³': 'ó'
}

def fix_mojibake(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for bad, good in replacements.items():
        content = content.replace(bad, good)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                fix_mojibake(os.path.join(root, file))
    print("Mojibake Fixed.")
