# AI / MLOps Portfolio

**Objetivo:** Convertirme en AI Engineer / MLOps Engineer mediante proyectos end-to-end con despliegue real, monitoreo y documentación profesional.

**Estado actual:** Fase 1 – Fundamentos de Python para datos y ML.

---
## Estructura del Proyecto
* **00_setup:** Configuración del entorno, Docker y herramientas.
* **01_python_data:** Notebooks de práctica con Pandas y NumPy.
* **datasets:** Archivos de datos locales para experimentos.
---
## Progreso del Proyecto
- [x] **Fase 0:** Setup del entorno (Python, Conda, Docker).
- [x] **Fase 1:** Fundamentos de Python para Datos.
                - [x] 1.3 Transformaciones y agregaciones.
                  - ##Insights: 1. Los clientes que abandonan la empresa (Churn) llaman en promedio 2.2 veces a soporte, comparado con 1.4 veces de los clientes  leales.
                  - 2. El gasto promedio de los clientes que se van es mayor ($65 vs $58).
                
                - [x] 1.4 Operaciones avanzadas y automatización (Script ETL)
                  - Implementación de `scripts/etl.py` para procesamiento por línea de comandos.
                  - Uso de operaciones vectorizadas para optimizar el rendimiento.
        
        - Habilidades Técnicas Demostradas:
        
        - Limpieza de datos con Pandas.
        - Automatización mediante scripts ETL.
        - Análisis de bases de datos relacionales con SQLite y SQL Avanzado.

- [x] Fase 1.6: Machine Learning Baseline.
    - Implementación de `Random Forest` con balanceo de clases.
    - Métricas obtenidas: **95% Accuracy** y **78.2% F1-Score** (promedio en CrossValidation/ CV).
    - Exportación de artefactos: Modelo y Escalador guardados en `/models` para despliegue.

  - ### 📈 Comparativa de Modelos
  - 
En esta fase evaluamos dos aproximaciones para establecer nuestra línea base (baseline):

| Modelo |                 Accuracy | Recall (Clase: Fuga) | F1-Score | Notas                                          |
 **Logistic Regression** | 86%      | 21%                  | 31%      | Muy débil detectando fugas reales.             |
 **Random Forest**       | **95%**  | **67%**              | **80%**  | **Modelo elegido.** Alta precisión y robustez. |

> **Insight:** El cambio a Random Forest junto con el balanceo de clases permitió triplicar la capacidad del modelo para identificar clientes en riesgo de abandono comparado con el anterior modelo utilizado de regresion logistica.

> ### 🔧 Fase 1.6.1: Optimización de Hyperparámetros
Se utilizó `GridSearchCV` para encontrar la configuración óptima del bosque, logrando reducir el sobreajuste (overfitting).

- **Mejor Configuración:** `max_depth: 10`, `n_estimators: 200`.
- **Resultado Final (F1-Score):** **83.71%** (Mejora del ~5% sobre el baseline).
- **Estado:** Modelo listo para la fase de MLOps y Despliegue.
- 
- [x] **Fase 1.7: Automatización y Cierre de Fase**
    - [x] Creación de `scripts/run_train.py` para entrenamiento reproducible.
    - [x] Implementación de **SMOTE** para balanceo de clases.
    - [x] Generación de `requirements.txt` para portabilidad.
    - [x] **Métrica Final:** F1-Score del **82%** (Logrando un Recall del 83% en fugas).
    - [x] Artefactos exportados: `model_v1.joblib` y `scaler_v1.joblib`.

- [x] **Fase 2: Transformers Intro**
    - Implementación de Pipeline de Sentimiento con `distilbert-base-uncased`.
    - Tiempo de inferencia detectado: **~0.039s** (Inferencia en CPU).
    - Pruebas exitosas detectando polaridad en frases de prueba.

- [x] **Fase 2.3: Embeddings y Almacenamiento**
    - Generación de embeddings densos (384 dimensiones) usando `all-MiniLM-L6-v2`.
    - Procesamiento de un lote de 100 documentos sintéticos de quejas de clientes.
    - Almacenamiento persistente de vectores en formato `.npy` y metadatos en `.parquet`.

- [x] **Fase 2.4: Vector Database (ChromaDB)**
    - Implementación de base de datos vectorial local con **ChromaDB**.
    - Indexación exitosa de 100 vectores con sus respectivos IDs y documentos.
    - **Métrica de Latencia de Búsqueda:** **0.045s** (Búsqueda semántica top-3).
    - Capacidad de recuperación demostrada: El sistema identifica "internet speed" como concepto relacionado a "slow connection". 
  
- [x] **Fase 2.5: RAG Simple (Pipeline Completo)**
    - Implementación de arquitectura **Retrieval-Augmented Generation**.
    - Integración de **ChromaDB** como recuperador de contexto y **Flan-T5** como generador de respuestas.
    - Creación de `scripts/rag_service.py`: Un servicio modular y portable que utiliza rutas absolutas para mayor robustez.
    - **Resultado:** El sistema es capaz de responder preguntas sobre problemas técnicos basándose exclusivamente en el contexto recuperado (evitando alucinaciones básicas).

---
## 🛠️ Tecnologías Fase 2
* **Modelos:** `sentence-transformers` (Embeddings), `Flan-T5-Small` (Generación).
* **Vector DB:** ChromaDB (Local Persistence).
* **Lógica:** Python orientado a objetos para el servicio RAG.
              