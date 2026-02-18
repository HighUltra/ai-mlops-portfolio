import os
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class RAGSystem:
    def __init__(self, model_name="google/flan-t5-small"):
        # 1. Obtener la ruta absoluta de la carpeta del proyecto
        # Esto detecta dónde está el script y sube un nivel a la raíz
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, "outputs", "chroma_db")
        
        print(f"📂 Buscando base de datos en: {db_path}")

        # 2. Inicializar cliente
        self.client = chromadb.PersistentClient(path=db_path)
        
        # 3. Intentar obtener la colección (usamos get_or_create para evitar errores)
        try:
            self.collection = self.client.get_collection(name="customer_complaints")
            print("✅ Colección encontrada con éxito.")
        except Exception as e:
            print(f"❌ Error: La colección no existe en esa ruta. {e}")
            raise
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def ask(self, question, k=3):
        # 1. Retrieval
        query_vector = self.embed_model.encode([question])[0].tolist()
        results = self.collection.query(query_embeddings=[query_vector], n_results=k)
        context = " ".join(results['documents'][0])
        
      # 2. Prompt
        prompt = f"""
        Answer the following question using ONLY the provided context. 
        If the answer is not in the context, say "I don't know".
        Keep the answer short but use complete sentences. Do not return IDs.

        Context: 
        {context}

        Question: {question}
        Helpful Answer:"""
        

        # 3. Inference
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=50)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Prueba rápida al ejecutar el script
    rag = RAGSystem()
    query = "What's wrong with the internet?"
    print(f"Query: {query}")
    print(f"Response: {rag.ask(query)}")