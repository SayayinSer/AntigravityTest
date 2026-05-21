import re
import uuid

# Read the clean template XML
with open(r"d:\aaProyectos\Entorno04\Temp\ConceptosCajaClean.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

guids_to_replace = {}

# Match all objects
# <Object ... guid="GUID" name="NAME" ...>
pattern = r'<Object[^>]*guid="([^"]+)"[^>]*name="([^"]+)"'
matches = re.findall(pattern, xml_content)

print(f"Found {len(matches)} objects in clean XML.")

for old_guid, name in matches:
    # We only want to replace GUIDs of our custom objects, not standard GeneXus ones.
    # Our objects start with ConceptosCaja or API_ConceptosCaja.
    if "ConceptosCaja" in name or "ConceptoCaja" in name:
        new_guid = str(uuid.uuid4())
        guids_to_replace[old_guid] = new_guid
        print(f"Mapping Object {name} ({old_guid}) -> ({new_guid})")

# Replace all occurrences of the old GUIDs with the new GUIDs
for old_guid, new_guid in guids_to_replace.items():
    xml_content = xml_content.replace(old_guid, new_guid)

# Perform text replacement for names
# Plural Zonas as requested by the user for the API Object
xml_content = xml_content.replace("API_ConceptosCaja", "API_Zonas")
xml_content = xml_content.replace("ConceptosCaja", "Zona")
xml_content = xml_content.replace("ConceptoCaja", "Zona")
xml_content = xml_content.replace("CONCEPTOSCAJA", "ZONA")

# Write output
with open(r"d:\aaProyectos\Entorno04\Envio_XPZ\API_Zonas_V4.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

print("Generated API_Zonas_V4.xml safely with new GUIDs from clean export.")
