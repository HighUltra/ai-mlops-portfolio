from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel # Esto es para el "contrato"
from scripts.rag_service import RAGSystem
import uvicorn

# 1. Definimos el MODELO de respuesta (El contrato)
class RAGResponse(BaseModel):
    status: str
    query: str
    answer: str
    model_info: str

app = FastAPI(
    title="Servicio de IA de Soporte",
    description="API robusta para consultas técnicas",
    version="1.1.0"
)

# Cargamos el sistema
try:
    rag = RAGSystem()
except Exception as e:
    print(f"❌ Error crítico cargando RAG: {e}")
    rag = None
    
@app.get("/")
def home():
    return {"message": "AI Support API is Online", "status": "Ready"}

@app.get("/ask", response_model=RAGResponse, tags=["IA Engine"])
def ask_ai(question: str = Query(..., min_length=3, description="Tu pregunta técnica")):
    """
    Endpoint robusto que garantiza una estructura de respuesta fija.
    """
    if not rag:
        raise HTTPException(status_code=500, detail="El motor de IA no está disponible")
    
    try:
        answer = rag.ask(question)
        
        # Retornamos siguiendo el "contrato" de RAGResponse
        return RAGResponse(
            status="success",
            query=question,
            answer=answer,
            model_info="Flan-T5-Small + ChromaDB"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la inferencia: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)