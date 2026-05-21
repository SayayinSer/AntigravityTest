import os
import re

kb_name = "77Lab"
kb_root = r"d:\aaProyectos\Entorno04"
shared_skills_root = r"d:\aaProyectos\Entorno04\.agents\skills"
examples_dir = os.path.join(shared_skills_root, "xpz-kb-parallel-setup", "examples")
scripts_dir = os.path.join(kb_root, "scripts")

if not os.path.exists(scripts_dir):
    os.makedirs(scripts_dir)

# List of wrappers to generate
wrappers = [
    "Update-KbFromXpz.example.ps1",
    "Test-KbFullSnapshot.example.ps1",
    "Query-KbIntelligence.example.ps1",
    "Rebuild-KbIntelligenceIndex.example.ps1",
    "Test-KbGate.example.ps1",
    "Get-KbMetadata.example.ps1",
    "Test-KbMetadataWrapper.example.ps1",
    "Test-KbSetupAudit.example.ps1",
    "Test-KbStructure.example.ps1"
]

for example_name in wrappers:
    source_path = os.path.join(examples_dir, example_name)
    if not os.path.exists(source_path):
        print(f"Example not found: {source_path}")
        continue
    
    target_name = example_name.replace("Kb", f"{kb_name}Kb").replace(".example", "")
    target_path = os.path.join(scripts_dir, target_name)
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace SharedSkillsRoot hardcoded values
    content = content.replace('SharedSkillsRoot = "C:\\CAMINHO\\PARA\\GeneXus-XPZ-Skills"', f'SharedSkillsRoot = "{shared_skills_root}"')
    content = content.replace('SharedSkillsRoot = "C:/CAMINHO/PARA/GeneXus-XPZ-Skills"', f'SharedSkillsRoot = "{shared_skills_root}"')
    
    # 2. Replace script names in strings (case insensitive)
    for other_example in wrappers:
        old_script = other_example.replace(".example", "")
        new_script = old_script.replace("Kb", f"{kb_name}Kb")
        content = re.sub(re.escape(old_script), new_script, content, flags=re.IGNORECASE)

    # 3. Standardize paths for scripts-xpz
    content = re.sub(r'scripts\\(?=gx-object|Sync-GeneXus|Build-Kb|Query-Kb|Test-Xpz|Test-GeneXus)', r'scripts-xpz\\', content, flags=re.IGNORECASE)
    content = re.sub(r'scripts/(?=gx-object|Sync-GeneXus|Build-Kb|Query-Kb|Test-Xpz|Test-GeneXus)', r'scripts-xpz/', content, flags=re.IGNORECASE)
    
    # 4. Fix folder names in strings: ensure KbIntelligence is used for folders
    # (re.sub might have replaced 'Kb' in 'KbIntelligence' if it was part of a script name, 
    # but KbIntelligence is usually a folder)
    # Actually, we want to ensure any '77LabKbIntelligence' that refers to a folder becomes 'KbIntelligence'
    content = content.replace(f"{kb_name}KbIntelligence", "KbIntelligence")
    
    # 5. Fix variable resolution ($repoRoot)
    content = content.replace("$repoRoot = Split-Path -Parent $PSScriptRoot", f"$KbRoot = Split-Path -Parent $PSScriptRoot\n$repoRoot = $KbRoot\n$SharedSkillsRoot = \"{shared_skills_root}\"")
    content = content.replace("$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)", f"$KbRoot = Split-Path -Parent $PSScriptRoot\n$repoRoot = $KbRoot\n$SharedSkillsRoot = \"{shared_skills_root}\"")

    # 6. Final fix for Test-KbStructure specifically
    if f"Test-{kb_name}KbStructure.ps1" in target_path:
        content = content.replace("Join-Path $SharedSkillsRoot 'scripts-xpz\\\\gx-object-type-catalog.json'", "Join-Path $SharedSkillsRoot 'scripts-xpz\\\\gx-object-type-catalog.json'")
        # Ensure it uses the right shared root
        content = content.replace("Join-Path $SharedSkillsRoot 'scripts-xpz\\\\gx-object-type-catalog.json'", f"Join-Path \"{shared_skills_root}\" 'scripts-xpz\\\\gx-object-type-catalog.json'")

    with open(target_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(content)
    
    print(f"Generated: {target_path}")

print("Done.")
