import uuid
from datetime import datetime

def guid():
    return str(uuid.uuid4())

def get_xml():
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.0000000Z')
    
    # We will generate the XML string for the objects:
    # 1. Zona_SDT
    # 2. ZonaListaSDT
    # 3. ZonaLista_DP
    # 4. Zona_DP
    # 5. Zona_Insertar
    # 6. Zona_Modificar
    # 7. Zona_Borrar
    # 8. API_Zona
    
    # We'll use dummy guids for the parent folder since we can just use the module Root Module
    api_folder_guid = guid()
    
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ExportFile>
  <KMW>
    <MajorVersion>4</MajorVersion>
    <MinorVersion>0</MinorVersion>
    <Build>177934</Build>
  </KMW>
  <Source kb="de91de00-b1a5-44d5-ab28-688adbfc8818" username="FACTORIAGX\Sergio" UNCPath="\\\\FACTORIAGX\D$\Models\\77Lab\\AngularV1">
    <Version guid="1088064f-70c6-44cf-9547-5f15d79570b7" name="AngularV1" />
  </Source>
  <Objects>
"""

    # SDT: Zona_SDT
    zona_sdt_guid = guid()
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="Zona_SDT" guid="{zona_sdt_guid}" name="Zona_SDT" type="447527b5-9210-4523-898b-5dccb17be60a" description="Recupera Informacion Zona">
      <Part type="5c2aa9da-8fc4-4b6b-ae02-8db4fa48976a">
        <Level Name="Zona_SDT">
          <LevelInfo guid="{guid()}" name="Zona_SDT" type="a76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>Zona_SDT</Value></Property></Properties>
          </LevelInfo>
          <Item guid="{guid()}" name="ZonaCodigo" type="f76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>ZonaCodigo</Value></Property><Property><Name>idBasedOn</Name><Value>Attribute:ZonaCodigo</Value></Property></Properties>
          </Item>
          <Item guid="{guid()}" name="ZonaNombre" type="f76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>ZonaNombre</Value></Property><Property><Name>idBasedOn</Name><Value>Attribute:ZonaNombre</Value></Property></Properties>
          </Item>
          <Item guid="{guid()}" name="ExisteSioNo" type="f76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>ExisteSioNo</Value></Property><Property><Name>idBasedOn</Name><Value>Domain:SioNo</Value></Property></Properties>
          </Item>
        </Level>
      </Part>
    </Object>
"""

    # SDT: ZonaListaSDT
    zona_lista_sdt_guid = guid()
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="ZonaListaSDT" guid="{zona_lista_sdt_guid}" name="ZonaListaSDT" type="447527b5-9210-4523-898b-5dccb17be60a" description="Lista de Zonas">
      <Part type="5c2aa9da-8fc4-4b6b-ae02-8db4fa48976a">
        <Level Name="ZonaListaSDT">
          <LevelInfo guid="{guid()}" name="ZonaListaSDT" type="a76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>ZonaListaSDT</Value></Property><Property><Name>AttCollection</Name><Value>True</Value></Property></Properties>
          </LevelInfo>
          <Item guid="{guid()}" name="ZonaCodigo" type="f76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>ZonaCodigo</Value></Property><Property><Name>idBasedOn</Name><Value>Attribute:ZonaCodigo</Value></Property></Properties>
          </Item>
          <Item guid="{guid()}" name="ZonaNombre" type="f76e9340-bdb9-445d-8f81-cfd4ddd0b0f3">
            <Properties><Property><Name>Name</Name><Value>ZonaNombre</Value></Property><Property><Name>idBasedOn</Name><Value>Attribute:ZonaNombre</Value></Property></Properties>
          </Item>
        </Level>
      </Part>
    </Object>
"""

    # Data Provider: Zona_DP
    zona_dp_guid = "c8cffbe9-8464-4acc-a148-162f95ab4c6b"
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="Zona_DP" guid="{zona_dp_guid}" name="Zona_DP" type="c9584656-94b6-4ccd-890f-332d11fc2c25" description="Recupera Zona">
      <Part type="9b0a32a3-de6d-4be1-a4dd-1b85d3741534">
        <Source><![CDATA[Zona_SDT
{{
    ZonaCodigo = ZonaCodigo
    ZonaNombre = ZonaNombre
    ExisteSioNo = "SI"
}}]]></Source>
      </Part>
      <Part type="c44bd5ff-f918-415b-98e6-aca44fed84fa">
        <Source><![CDATA[parm(in:&Buscar_ZonaCodigo);]]></Source>
      </Part>
      <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
        <Variable Name="Buscar_ZonaCodigo">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaCodigo</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Character</Value></Property><Property><Name>Length</Name><Value>20</Value></Property></Properties>
        </Variable>
      </Part>
      <Properties>
        <Property><Name>IsDefault</Name><Value>False</Value></Property>
      </Properties>
    </Object>
"""

    # Data Provider: ZonaLista_DP
    zona_lista_dp_guid = "acefd507-9137-4ff9-84ac-44c5993465b1"
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="ZonaLista_DP" guid="{zona_lista_dp_guid}" name="ZonaLista_DP" type="c9584656-94b6-4ccd-890f-332d11fc2c25" description="Lista de Zonas DP">
      <Part type="9b0a32a3-de6d-4be1-a4dd-1b85d3741534">
        <Source><![CDATA[ZonaListaSDT
{{
    ZonaListaSDTItem
    where ZonaNombre like &Buscar_ZonaNombre when not &Buscar_ZonaNombre.IsEmpty()
    {{
        ZonaCodigo = ZonaCodigo
        ZonaNombre = ZonaNombre
    }}
}}]]></Source>
      </Part>
      <Part type="c44bd5ff-f918-415b-98e6-aca44fed84fa">
        <Source><![CDATA[parm(in:&Buscar_ZonaNombre);]]></Source>
      </Part>
      <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
        <Variable Name="Buscar_ZonaNombre">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaNombre</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:VarChar</Value></Property><Property><Name>Length</Name><Value>60</Value></Property></Properties>
        </Variable>
      </Part>
    </Object>
"""

    # Procedure: Zona_Insertar
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="Zona_Insertar" guid="bb742e80-14ac-4b9e-b58e-839776d401c8" name="Zona_Insertar" type="84a12143-3242-4a54-939e-64d054572011" description="Insertar Zona">
      <Part type="9b0a32a3-de6d-4be1-a4dd-1b85d3741534">
        <Source><![CDATA[&Zona = new()
&Zona.ZonaCodigo = &Buscar_ZonaCodigo
&Zona.ZonaNombre = &Buscar_ZonaNombre
&Zona.Save()
if &Zona.Success()
  commit
else
  &Messages = &Zona.GetMessages()
  rollback
endif]]></Source>
      </Part>
      <Part type="c44bd5ff-f918-415b-98e6-aca44fed84fa">
        <Source><![CDATA[parm(in:&Buscar_ZonaCodigo, in:&Buscar_ZonaNombre, out:&Messages);]]></Source>
      </Part>
      <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
        <Variable Name="Zona">
          <Properties><Property><Name>Name</Name><Value>Zona</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bc:Zona</Value></Property></Properties>
        </Variable>
        <Variable Name="Messages">
          <Properties><Property><Name>Name</Name><Value>Messages</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Messages</Value></Property><Property><Name>IsCollection</Name><Value>True</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaCodigo">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaCodigo</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Character</Value></Property><Property><Name>Length</Name><Value>20</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaNombre">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaNombre</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:VarChar</Value></Property><Property><Name>Length</Name><Value>60</Value></Property></Properties>
        </Variable>
      </Part>
    </Object>
"""

    # Procedure: Zona_Modificar
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="Zona_Modificar" guid="b448a2e3-7956-4882-b310-736788074011" name="Zona_Modificar" type="84a12143-3242-4a54-939e-64d054572011" description="Modificar Zona">
      <Part type="9b0a32a3-de6d-4be1-a4dd-1b85d3741534">
        <Source><![CDATA[&Zona.Load(&Buscar_ZonaCodigo)
if &Zona.Success()
  &Zona.ZonaNombre = &Buscar_ZonaNombre
  &Zona.Save()
  if &Zona.Success()
    commit
  else
    &Messages = &Zona.GetMessages()
    rollback
  endif
else
  &Messages = &Zona.GetMessages()
endif]]></Source>
      </Part>
      <Part type="c44bd5ff-f918-415b-98e6-aca44fed84fa">
        <Source><![CDATA[parm(in:&Buscar_ZonaCodigo, in:&Buscar_ZonaNombre, out:&Messages);]]></Source>
      </Part>
      <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
        <Variable Name="Zona">
          <Properties><Property><Name>Name</Name><Value>Zona</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bc:Zona</Value></Property></Properties>
        </Variable>
        <Variable Name="Messages">
          <Properties><Property><Name>Name</Name><Value>Messages</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Messages</Value></Property><Property><Name>IsCollection</Name><Value>True</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaCodigo">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaCodigo</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Character</Value></Property><Property><Name>Length</Name><Value>20</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaNombre">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaNombre</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:VarChar</Value></Property><Property><Name>Length</Name><Value>60</Value></Property></Properties>
        </Variable>
      </Part>
    </Object>
"""

    # Procedure: Zona_Borrar
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="Zona_Borrar" guid="c6c3b685-cc62-460d-96e0-fd36ebf37b46" name="Zona_Borrar" type="84a12143-3242-4a54-939e-64d054572011" description="Borrar Zona">
      <Part type="9b0a32a3-de6d-4be1-a4dd-1b85d3741534">
        <Source><![CDATA[&Zona.Load(&Buscar_ZonaCodigo)
if &Zona.Success()
  &Zona.Delete()
  if &Zona.Success()
    commit
  else
    &Messages = &Zona.GetMessages()
    rollback
  endif
else
  &Messages = &Zona.GetMessages()
endif]]></Source>
      </Part>
      <Part type="c44bd5ff-f918-415b-98e6-aca44fed84fa">
        <Source><![CDATA[parm(in:&Buscar_ZonaCodigo, out:&Messages);]]></Source>
      </Part>
      <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
        <Variable Name="Zona">
          <Properties><Property><Name>Name</Name><Value>Zona</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bc:Zona</Value></Property></Properties>
        </Variable>
        <Variable Name="Messages">
          <Properties><Property><Name>Name</Name><Value>Messages</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Messages</Value></Property><Property><Name>IsCollection</Name><Value>True</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaCodigo">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaCodigo</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Character</Value></Property><Property><Name>Length</Name><Value>20</Value></Property></Properties>
        </Variable>
      </Part>
    </Object>
"""

    # API Object: API_Zona
    api_zona_guid = guid()
    xml += f"""
    <Object user="FACTORIAGX\Sergio" versionDate="0001-01-01T00:00:00.0000000" lastUpdate="{now}" fullyQualifiedName="API_Zona" guid="{api_zona_guid}" name="API_Zona" type="dcd3395a-7fcd-400a-867f-94a50d242555" description="API para Zona">
      <Part type="d24a58ad-57ba-41b7-9e6e-eaca3543c778">
        <Source><![CDATA[Service Zonas
{{
    [Description("Recupera la Lista de Zonas cargadas.")]
    [RestMethod(GET)]
    Listar(in:&Buscar_ZonaNombre, out:&ZonaListaSDT) => ZonaLista_DP(in:&Buscar_ZonaNombre, out:&ZonaListaSDT);

    [Description("Recupera una Zona")]
    [RestMethod(GET)]
    Buscar(in:&Buscar_ZonaCodigo, out:&Zona_SDT) => Zona_DP(in:&Buscar_ZonaCodigo, out:&Zona_SDT);

    [Description("Graba una Nueva Zona")]
    [RestMethod(POST)]
    Insertar(in:&Buscar_ZonaCodigo, in:&Buscar_ZonaNombre, out:&Messages) => Zona_Insertar(in:&Buscar_ZonaCodigo, in:&Buscar_ZonaNombre, out:&Messages);

    [Description("Modificar una Zona existente")]
    [RestMethod(PUT)]
    Modificar(in:&Buscar_ZonaCodigo, in:&Buscar_ZonaNombre, out:&Messages) => Zona_Modificar(in:&Buscar_ZonaCodigo, in:&Buscar_ZonaNombre, out:&Messages);

    [Description("Borrar una Zona existente")]
    [RestMethod(DELETE)]
    Borrar(in:&Buscar_ZonaCodigo, out:&Messages) => Zona_Borrar(in:&Buscar_ZonaCodigo, out:&Messages);
}}]]></Source>
      </Part>
      <Part type="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
        <Variable Name="ZonaListaSDT">
          <Properties><Property><Name>Name</Name><Value>ZonaListaSDT</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>sdt:ZonaListaSDT</Value></Property></Properties>
        </Variable>
        <Variable Name="Zona_SDT">
          <Properties><Property><Name>Name</Name><Value>Zona_SDT</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>sdt:Zona_SDT</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaCodigo">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaCodigo</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Character</Value></Property><Property><Name>Length</Name><Value>20</Value></Property></Properties>
        </Variable>
        <Variable Name="Buscar_ZonaNombre">
          <Properties><Property><Name>Name</Name><Value>Buscar_ZonaNombre</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:VarChar</Value></Property><Property><Name>Length</Name><Value>60</Value></Property></Properties>
        </Variable>
        <Variable Name="Messages">
          <Properties><Property><Name>Name</Name><Value>Messages</Value></Property><Property><Name>idATTCUSTOMTYPE</Name><Value>bas:Messages</Value></Property><Property><Name>IsCollection</Name><Value>True</Value></Property></Properties>
        </Variable>
      </Part>
      <Properties>
         <Property><Name>Name</Name><Value>API_Zona</Value></Property>
      </Properties>
    </Object>
"""

    xml += """
  </Objects>
  <Dependencies>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Object" Id="447527b5-9210-4523-898b-5dccb17be60a">
      <Properties Name="Structured Data Type" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Part" Id="5c2aa9da-8fc4-4b6b-ae02-8db4fa48976a">
      <Properties Name="Structure" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Object" Id="c9584656-94b6-4ccd-890f-332d11fc2c25">
      <Properties Name="Data Provider" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Object" Id="84a12143-3242-4a54-939e-64d054572011">
      <Properties Name="Procedure" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Object" Id="dcd3395a-7fcd-400a-867f-94a50d242555">
      <Properties Name="API" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Part" Id="9b0a32a3-de6d-4be1-a4dd-1b85d3741534">
      <Properties Name="Source" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Part" Id="c44bd5ff-f918-415b-98e6-aca44fed84fa">
      <Properties Name="Rules" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Part" Id="e4c4ade7-53f0-4a56-bdfd-843735b66f47">
      <Properties Name="Variables" PackageName="GenexusBL" />
    </Reference>
    <Reference Package="3ea7e1c6-b849-4df9-931a-070171a8a2f0" Type="Part" Id="d24a58ad-57ba-41b7-9e6e-eaca3543c778">
      <Properties Name="Events" PackageName="GenexusBL" />
    </Reference>
  </Dependencies>
</ExportFile>
"""
    
    with open("d:\\aaProyectos\\Entorno04\\Envio_XPZ\\API_Zona_V2.xml", "w", encoding="utf-8") as f:
        f.write(xml)

if __name__ == "__main__":
    get_xml()
    print("API_Zona_V2.xml generated successfully.")
