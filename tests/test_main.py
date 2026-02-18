from fastapi.testclient import TestClient
from App.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Verificamos que devuelva el mensaje de bienvenida
    assert response.json()["status"] == "Ready"

def test_ask_ai_valid():
    response = client.get("/ask?question=how to fix internet")
    assert response.status_code == 200
    # CAMBIO AQUÍ: Ya no buscamos dentro de ["data"], sino directo en el JSON
    json_response = response.json()
    assert "answer" in json_response
    assert json_response["status"] == "success"

def test_ask_ai_too_short():
    # Este ya pasaba, lo dejamos igual. Prueba la robustez de Pydantic.
    response = client.get("/ask?question=hi")
    assert response.status_code == 422