import re
import uuid

# Read the text-replaced XML
with open(r"d:\aaProyectos\Entorno04\Envio_XPZ\API_Zonas_V4.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

# Find all objects with "Zona" in their name
pattern = r'<Object[^>]*guid="([^"]+)"[^>]*name="([^"]*Zona[^"]*)"'
matches = re.findall(pattern, xml_content)

print(f"Found {len(matches)} objects to remap GUIDs.")

guids_to_replace = {}
for old_guid, name in matches:
    new_guid = str(uuid.uuid4())
    guids_to_replace[old_guid] = new_guid
    print(f"Mapping Object {name} ({old_guid}) -> ({new_guid})")

# Replace GUIDs
for old_guid, new_guid in guids_to_replace.items():
    xml_content = xml_content.replace(old_guid, new_guid)

# Write back
with open(r"d:\aaProyectos\Entorno04\Envio_XPZ\API_Zonas_V4.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

print("GUIDs remapped successfully in API_Zonas_V4.xml")
