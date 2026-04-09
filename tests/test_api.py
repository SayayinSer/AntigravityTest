from fastapi.testclient import TestClient
from app.main import app
import pytest

# Usamos una función para obtener un cliente limpio en cada prueba
@pytest.fixture
def client():
    return TestClient(app)

def test_login_success(client):
    response = client.post("/login", data={"username": "SU", "password": "123456"}, follow_redirects=True)
    assert response.status_code == 200
    # Verificamos que se redirigió al dashboard o que el contenido es del dashboard
    assert "ANTIGRAVITY" in response.text

def test_login_failure(client):
    response = client.post("/login", data={"username": "SU", "password": "wrongpassword"})
    assert response.status_code == 401

def test_unauthorized_admin_access(client):
    response = client.get("/admin/security", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["location"]

def test_restricted_role_access(client):
    # Loguear como operador
    client.post("/login", data={"username": "operador", "password": "123456"}, follow_redirects=True)
    # Intentar entrar a seguridad
    response = client.get("/admin/security")
    assert response.status_code == 403
