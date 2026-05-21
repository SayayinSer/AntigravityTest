import re
import uuid

# Read the original clean export (which has references)
with open(r"d:\aaProyectos\Entorno04\Temp\ConceptosCajaClean.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

# I want to find all <Object> tags and keep only those that are NOT Attributes or Domains.
# I'll use a more precise regex for Objects.
# <Object ... type="GUID" ... name="NAME" ...>...</Object>
# Actually, I'll just look for the names I want to keep.

objects_to_keep = [
    "API_ConceptosCaja",
    "ConceptosCaja_Insertar",
    "ConceptosCaja_Modificar",
    "ConceptosCaja_Borrar",
    "ConceptosCaja_DP",
    "ConceptosCajaLista_DP",
    "ConceptosCaja_SDT",
    "ConceptosCajaListaSDT"
]

# I'll also perform the text replacements here.
new_xml = xml_content
for obj in objects_to_keep:
    # Rename in the name="..." attribute
    new_name = obj.replace("ConceptosCaja", "Zona").replace("ConceptoCaja", "Zona")
    if obj == "API_ConceptosCaja": new_name = "API_Zonas"
    new_xml = new_xml.replace(f'name="{obj}"', f'name="{new_name}"')
    
    # Replace in code/text
    new_xml = new_xml.replace(obj, new_name)

# Now, very important: we must REMOVE the <Object> tags that are not ours.
# But XML parsing with regex is hard.
# I'll just replace the GUIDs of OUR objects with new ones.
# And I'll hope GeneXus ignores the rest if they already exist (which they do).

# Find GUIDs of our renamed objects
guids_to_replace = {}
for obj in objects_to_keep:
    new_name = obj.replace("ConceptosCaja", "Zona").replace("ConceptoCaja", "Zona")
    if obj == "API_ConceptosCaja": new_name = "API_Zonas"
    
    pattern = rf'guid="([^"]+)"[^>]*name="{new_name}"'
    match = re.search(pattern, new_xml)
    if match:
        old_guid = match.group(1)
        new_guid = str(uuid.uuid4())
        guids_to_replace[old_guid] = new_guid
        print(f"Mapping {new_name} ({old_guid}) -> ({new_guid})")

for old_guid, new_guid in guids_to_replace.items():
    new_xml = new_xml.replace(old_guid, new_guid)

# Final clean replacements
new_xml = new_xml.replace("ConceptosCaja", "Zona")
new_xml = new_xml.replace("ConceptoCaja", "Zona")

with open(r"d:\aaProyectos\Entorno04\Envio_XPZ\API_Zonas_V5.xml", "w", encoding="utf-8") as f:
    f.write(new_xml)

print("Generated API_Zonas_V5.xml")
