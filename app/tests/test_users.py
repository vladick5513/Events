import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("name,email,password, status_code",[
    ("bro", "test_user@example.com", "password123", 201),
    ("bro", "test_user@example.com", "password1234", 409),
    ("bro", "abcd", "password1234", 422),
])
async def test_register_user(ac:AsyncClient, prepare_database, name,email,password, status_code):
    response = await ac.post("/users/register", json={
        "name": name,"email": email, "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("valid_user@example.com", "password123", 200),  # Успешный вход
    ("valid_user@example.com", "wrongpassword", 401),  # Неверный пароль
    ("nonexistent_user@example.com", "password123", 401),  # Пользователь не существует
    ("invalidemail", "password123", 422),  # Неверный email-формат
])
async def test_login_user(ac: AsyncClient, create_test_user, email, password, status_code):
    """Параметризованный тест для входа."""
    if email == "valid_user@example.com":
        email = create_test_user["email"]

    response = await ac.post("/users/login", json={"email": email, "password": password})
    assert response.status_code == status_code

    if status_code == 200:
        assert "booking_access_token" in response.cookies
        assert isinstance(response.json(), str)
    else:
        assert "booking_access_token" not in response.cookies

