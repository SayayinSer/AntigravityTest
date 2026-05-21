import re
import uuid

# Read the template XML
with open(r"d:\aaProyectos\Entorno04\Temp\ConceptosCajaApi.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

guids_to_replace = {}

# Match all objects that have ConceptosCaja or ConceptoCaja in their name
# <Object ... guid="GUID" name="NAME" ...>
pattern = r'<Object[^>]*guid="([^"]+)"[^>]*name="([^"]*Concepto[s]?Caja[^"]*)"'
matches = re.findall(pattern, xml_content)

print(f"Found {len(matches)} objects via <Object> tags.")

for old_guid, name in matches:
    new_guid = str(uuid.uuid4())
    guids_to_replace[old_guid] = new_guid
    print(f"Mapping Object {name} ({old_guid}) -> ({new_guid})")

# Also match Parts and Levels inside those objects? 
# Wait, if we replace the Object GUID, we should also replace any GUIDs of its parts if they are referenced.
# Actually, the simplest is to just replace the Object GUIDs, and GeneXus will generate new GUIDs for the parts on import if needed.
# Let's also look for <Level ... Guid="GUID">
level_pattern = r'<Level[^>]*Name="([^"]*Concepto[s]?Caja[^"]*)"[^>]*Guid="([^"]+)"'
level_matches = re.findall(level_pattern, xml_content)
for name, old_guid in level_matches:
    if old_guid not in guids_to_replace:
        new_guid = str(uuid.uuid4())
        guids_to_replace[old_guid] = new_guid
        print(f"Mapping Level {name} ({old_guid}) -> ({new_guid})")

# Replace all occurrences of the old GUIDs with the new GUIDs
for old_guid, new_guid in guids_to_replace.items():
    xml_content = xml_content.replace(old_guid, new_guid)

# Perform text replacement for names
xml_content = xml_content.replace("ConceptosCaja", "Zona")
xml_content = xml_content.replace("ConceptoCaja", "Zona")
xml_content = xml_content.replace("CONCEPTOSCAJA", "ZONA")
xml_content = xml_content.replace("conceptoscaja", "zona")
xml_content = xml_content.replace("conceptocaja", "zona")

# Write output
with open(r"d:\aaProyectos\Entorno04\Envio_XPZ\API_Zona_V3.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

print("Generated API_Zona_V3.xml safely with new GUIDs.")
