import pytest
from app import auth

def test_password_hashing():
    password = "testpassword123"
    hashed = auth.get_password_hash(password)
    assert hashed != password
    assert auth.verify_password(password, hashed) is True
    assert auth.verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    data = {"sub": "testuser"}
    token = auth.create_access_token(data)
    assert token is not None
    assert isinstance(token, str)
