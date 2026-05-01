# db_wrapper.py (Python Database Access)
```python
import psycopg2
import mysql.connector
import pyodbc
from typing import Any, List

class DBWrapper:
    def __init__(self, engine: str, connection_string: str):
        self.engine = engine.lower()
        self.conn_str = connection_string
        self.conn = self._connect()

    def _connect(self):
        if self.engine == 'postgresql':
            return psycopg2.connect(self.conn_str)
        elif self.engine in ['mysql', 'mariadb']:
            return mysql.connector.connect(self.conn_str)
        elif self.engine == 'sqlserver':
            return pyodbc.connect(self.conn_str)
        raise ValueError(f"Engine {self.engine} not supported")

    def execute_query(self, sql: str, params: tuple = None) -> List[Any]:
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            if cursor.description:
                return cursor.fetchall()
            self.conn.commit()
            return []

# deploy_db.sh (Linux/MacOS Bash Deployment)
```bash
#!/bin/bash
# Script para ejecutar archivos SQL en lote (PostgreSQL)
DB_NAME="mi_database"
DB_USER="postgres"
SQL_FILES_DIR="./migrations"

echo "Iniciando despliegue de base de datos..."
for f in $SQL_FILES_DIR/*.sql
do
  echo "Ejecutando $f..."
  psql -d $DB_NAME -U $DB_USER -f $f
  if [ $? -ne 0 ]; then
    echo "ERROR al ejecutar $f. Abortando."
    exit 1
  fi
done
echo "Despliegue completado con éxito."
```

# deploy_db.ps1 (Windows PowerShell Deployment)
```powershell
# Script para ejecutar archivos SQL en lote (SQL Server)
$Server = "localhost"
$Database = "MiDB"
$SqlFilesDir = "./migrations"

Get-ChildItem -Path "$SqlFilesDir\*.sql" | ForEach-Object {
    Write-Host "Ejecutando $($_.Name)..."
    Invoke-Sqlcmd -ServerInstance $Server -Database $Database -InputFile $_.FullName
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Error en $($_.Name). Abortando."
        exit 1
    }
}
Write-Host "Proceso terminado."
```
