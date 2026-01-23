import pandas as pd
import os

def run_etl():
    print("Iniciando proceso ETL...")
    # 1. Cargar
    df = pd.read_csv('../datasets/churn.csv')
    
    # 2. Limpiar nombres de columnas (quitar el 'Total' si existe o corregir)
    df.columns = [c.replace('Total ', '') if 'Total ' in c else c for c in df.columns]
    
    # 3. Transformar
    df['Churn_Numeric'] = df['Churn?'].apply(lambda x: 1 if 'True' in str(x) else 0)
    cols_cargos = ['Day Charge', 'Eve Charge', 'Night Charge', 'Intl Charge']
    df['Total_Combined_Charge'] = df[cols_cargos].sum(axis=1)
    
    # 4. Guardar
    os.makedirs('../outputs', exist_ok=True)
    df.to_csv('../outputs/churn_processed.csv', index=False)
    print("✅ Proceso completado. Archivo guardado en outputs/churn_processed.csv")

if __name__ == "__main__":
    run_etl()
    
    
