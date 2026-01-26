import sqlite3
import pandas as pd

# 1. Crear la conexión a la base de datos (se creará un archivo llamado 'telecom.db')
conn = sqlite3.connect('../datasets/telecom.db')

# 2. Cargar nuestro CSV procesado
df = pd.read_csv('../outputs/churn_processed.csv')

# 3. "Inyectar" los datos a una tabla SQL llamada 'clientes'
# Si la tabla ya existe, la reemplaza
df.to_sql('clientes', conn, if_exists='replace', index=False)

print("✅ Base de datos 'telecom.db' creada y tabla 'clientes' cargada.")

# 4. Cerrar conexión por seguridad
conn.close()