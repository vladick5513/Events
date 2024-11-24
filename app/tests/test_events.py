import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("title,description,date,location, available_seats,status_code", [
    ("Concert", "A live concert event.", "2024-12-25", "New York", 50, 200),
    ("Short", "A short description.", "2024-12-25", "Chicago", 100, 200),
    ("No Description", None, "2024-12-25T19:00:00", "Chicago",52, 422),  # Ошибка, description обязателен
    ("", "Missing title.", "2024-12-25T19:00:00", "Chicago",52, 422),   # Ошибка, title обязателен
])
async def test_create_event(ac: AsyncClient, prepare_database, title, description, date, location, available_seats, status_code):
    response = await ac.post("/events", json={
        "title": title,
        "description": description,
        "date": date,
        "location": location,
        "available_seats":available_seats
    })
    assert response.status_code == status_code

    # if expected_status_code == 201:
    #     data = response.json()
    #     assert data["title"] == title
    #     assert data["description"] == description
    #     assert data["date"] == date
    #     assert data["location"] == location