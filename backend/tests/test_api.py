import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """Тестирование эндпоинта проверки работоспособности."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/health")
    
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "AI Culinary Assistant API"
    }

@pytest.mark.asyncio
async def test_recipes_validation_error():
    """Тест валидации: пустое тело запроса должно возвращать 422."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/recipes", json={"ingredients": []})
    
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_question_validation_error():
    """Тест валидации: пустой вопрос должен возвращать 422."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/question", json={"question": "   "})
    
    assert response.status_code == 422
