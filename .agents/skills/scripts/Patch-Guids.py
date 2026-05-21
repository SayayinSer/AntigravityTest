import re
import uuid

# Read the generated GUIDs from the GeneXus KB
with open(r"d:\aaProyectos\Entorno04\Temp\ZonaObjectsCreated.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

# Extract GUIDs
def extract_guid(name):
    match = re.search(f'guid="([^"]+)" name="{name}"', xml_content)
    if match:
        return match.group(1)
    return str(uuid.uuid4())

zona_dp_guid = extract_guid("Zona_DP")
zonalista_dp_guid = extract_guid("ZonaLista_DP")
zona_insertar_guid = extract_guid("Zona_Insertar")
zona_modificar_guid = extract_guid("Zona_Modificar")
zona_borrar_guid = extract_guid("Zona_Borrar")

# Update Generate-ZonaApi.py
with open(r"d:\aaProyectos\Entorno04\scripts\Generate-ZonaApi.py", "r", encoding="utf-8") as f:
    script_content = f.read()

# Replace the random GUID generation for these specific objects
script_content = script_content.replace('zona_dp_guid = guid()', f'zona_dp_guid = "{zona_dp_guid}"')
script_content = script_content.replace('zona_lista_dp_guid = guid()', f'zona_lista_dp_guid = "{zonalista_dp_guid}"')
script_content = script_content.replace('fullyQualifiedName="Zona_Insertar" guid="{guid()}"', f'fullyQualifiedName="Zona_Insertar" guid="{zona_insertar_guid}"')
script_content = script_content.replace('fullyQualifiedName="Zona_Modificar" guid="{guid()}"', f'fullyQualifiedName="Zona_Modificar" guid="{zona_modificar_guid}"')
script_content = script_content.replace('fullyQualifiedName="Zona_Borrar" guid="{guid()}"', f'fullyQualifiedName="Zona_Borrar" guid="{zona_borrar_guid}"')

with open(r"d:\aaProyectos\Entorno04\scripts\Generate-ZonaApi.py", "w", encoding="utf-8") as f:
    f.write(script_content)

print("Generate-ZonaApi.py patched with actual KB GUIDs successfully.")
