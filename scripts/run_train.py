import pandas as pd
import joblib
import os
import mlflow  # <--- 1. Importamos la librería
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo en {file_path}. ¿Corriste el ETL?")
    return pd.read_csv(file_path)

def train_model():
    # --- 2. CONFIGURACIÓN DE MLFLOW ---
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Churn_Prediction_Project")

    # Todo lo que pase dentro del "with" se registrará automáticamente
    with mlflow.start_run(run_name="RF_v1_Con_Smote"):
        
        # 1. Cargar datos
        df = load_data('../outputs/churn_processed.csv')
        df = df.drop(['Phone', 'Churn?'], axis=1, errors='ignore')
        
        # 2. Preparar X e y
        df_encoded = pd.get_dummies(df, drop_first=True)
        target_cols = [c for c in df_encoded.columns if 'Churn' in c]
        if not target_cols:
            raise ValueError("No se encontró la columna de Churn.")
        
        target_col = target_cols[0]
        X = df_encoded.drop([target_col], axis=1)
        y = df_encoded[target_col]
        
        # 3. Escalado y Balanceo
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X_scaled, y)
        
        # --- 3. REGISTRAR PARÁMETROS EN MLFLOW ---
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("use_smote", True)
        
        # 4. Entrenamiento
        model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
        model.fit(X_res, y_res)
        
        # Calcular una métrica rápida para MLflow
        accuracy = model.score(X_scaled, y) # Una métrica de ejemplo
        mlflow.log_metric("accuracy_entrenamiento", accuracy)

        # 5. Guardar resultados (Tus archivos locales de siempre)
        os.makedirs('../models', exist_ok=True)
        joblib.dump(model, '../models/model_v1.joblib')
        joblib.dump(scaler, '../models/scaler_v1.joblib')
        
        # --- 4. GUARDAR MODELO EN MLFLOW ---
        mlflow.sklearn.log_model(model, "random_forest_model")
        
        print(f"✅ Entrenamiento exitoso y registrado en MLflow (Acc: {accuracy:.2f})")

if __name__ == "__main__":
    train_model()