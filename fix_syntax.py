import os
import re

VIEWS_DIR = "d:\\aaProyectos\\Entorno01\\NucleoTallerPHP\\src\\Views"

def final_cleanup(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert the if replacement mess
    content = content.replace('<?php ? ', '<?php if ')
    content = content.replace('<?php  ? ', '<?php if ')
    
    # Fix the $""->format mess
    content = re.sub(r'\$""->format\((.*?)\)', r'number_format(\1, 2)', content)
    
    # Fix missing $ in common variables
    vars_to_fix = ['apt', 'uapt', 'order', 'v', 'u', 'user', 'ot', 'p', 't', 'tk', 
                   'today_appointments', 'upcoming_appointments', 'vehicles', 'clients', 'active_page']
    for v in vars_to_fix:
        # Match v only if it's not preceded by $ and not part of another word
        content = re.sub(r'(?<![\$\w])' + v + r'(->|\b)', r'$' + v + r'\1', content)

    # Fix logic operators
    content = content.replace(' and ', ' && ')
    content = content.replace(' or ', ' || ')
    
    # Fix includes
    content = re.sub(r"\{% include '(.*?)' %\}", r"<?php include BASE_PATH . 'src/Views/\1.view.php'; ?>", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for root, dirs, files in os.walk(VIEWS_DIR):
        for file in files:
            if file.endswith('.php'):
                final_cleanup(os.path.join(root, file))
    print("Final Cleanup Applied.")
