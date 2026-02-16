import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """Carga el dataset generado por el ETL."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo en {file_path}. ¿Corriste el ETL?")
    return pd.read_csv(file_path)

def train_model():
    # 1. Cargar datos
    df = load_data('../outputs/churn_processed.csv')
    
    df = df.drop(['Phone', 'Churn?'], axis=1)
    
    # 2. Preparar X e y (Asegúrate de que estas columnas existan en tu CSV)
    # Aquí aplicamos el Encoding si no estaba listo
    df_encoded = pd.get_dummies(df, drop_first=True)
    
    print("Columnas detectadas después del Encoding:")
    print(df_encoded.columns.tolist())
    
  # Buscamos la columna objetivo automáticamente (la que tenga "Churn")
    target_cols = [c for c in df_encoded.columns if 'Churn' in c]
    if not target_cols:
        raise ValueError("No se encontró la columna de Churn. Revisa el CSV.")
    
    target_col = target_cols[0]
    print(f"🎯 Variable objetivo detectada: {target_col}")

    X = df_encoded.drop([target_col], axis=1)
    y = df_encoded[target_col]
    
    # 3. Escalado y Balanceo (SMOTE)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_scaled, y)
    
    # 4. Entrenamiento con los mejores parámetros que encontramos
    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_res, y_res)
    
    # 5. Guardar resultados (Artifacts)
    os.makedirs('../models', exist_ok=True)
    joblib.dump(model, '../models/model_v1.joblib')
    joblib.dump(scaler, '../models/scaler_v1.joblib')
    
    print("✅ Entrenamiento exitoso. Modelo 'v1' actualizado con SMOTE.")

if __name__ == "__main__":
    train_model()