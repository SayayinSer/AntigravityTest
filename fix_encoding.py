import os

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src"

def fix_encoding(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Remove BOM if exists
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
            
        # Try to decode as utf-8, if it fails, it might be latin-1
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('latin-1')
            
        # Save back as pure UTF-8 without BOM
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                fix_encoding(os.path.join(root, file))
    
    # Also fix index.php in public
    fix_encoding("d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\public\\index.php")
    print("Encoding Enforced to UTF-8 (No BOM).")
