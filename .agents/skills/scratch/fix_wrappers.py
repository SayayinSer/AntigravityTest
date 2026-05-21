import os

kb_root = r"d:\aaProyectos\Entorno04"
scripts_dir = os.path.join(kb_root, "scripts")
shared_skills_root = r"d:\aaProyectos\Entorno04\.agents\skills"

for filename in os.listdir(scripts_dir):
    if not filename.endswith(".ps1"):
        continue
    
    path = os.path.join(scripts_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Correct the SharedSkillsRoot and scripts-xpz paths
    # Ensure it's .agents\skills\scripts-xpz
    
    # Case 1: Join-Path $SharedSkillsRoot 'scripts-xpz\...'
    # Case 2: Join-Path $repoRoot 'scripts-xpz\...' -> WRONG
    
    content = content.replace("Join-Path $repoRoot 'scripts-xpz", "Join-Path $SharedSkillsRoot 'scripts-xpz")
    content = content.replace("Join-Path $repoRoot \"scripts-xpz", "Join-Path $SharedSkillsRoot \"scripts-xpz")
    
    # Fix script name references that might have been missed
    content = content.replace("Query-KbIntelligence.ps1", "Query-77LabKbIntelligence.ps1")
    content = content.replace("Rebuild-KbIntelligenceIndex.ps1", "Rebuild-77LabKbIntelligenceIndex.ps1")
    
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(content)

print("Done.")
