# ============================================
# MAIN APP - Flask сервер (главный файл)
# ============================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from recipes import recipe_manager
from config import config

# Создаем Flask приложение
app = Flask(__name__)

# Включаем CORS (разрешаем запросы с других доменов)
CORS(app, origins=config.CORS_ORIGINS)

# ============================================
# ROUTES (Маршруты/Endpoints)
# ============================================

@app.route('/api/health', methods=['GET'])
def health():
    """
    Проверка, работает ли сервер
    
    Response:
        {
            "status": "ok",
            "message": "Server is running"
        }
    """
    return jsonify({
        "status": "ok",
        "message": "Server is running"
    }), 200


@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    """
    Получить рецепты по ингредиентам
    
    Request body:
        {
            "ingredients": ["яйцо", "масло", "мука"]
        }
    
    Response:
        {
            "success": true,
            "ingredients": ["яйцо", "масло", "мука"],
            "recipes": "Рецепты..."
        }
    """
    
    # Получаем данные из запроса
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    ingredients = data.get('ingredients', [])
    
    # Получаем рецепты через менеджер
    result = recipe_manager.get_recipes_by_ingredients(ingredients)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@app.route('/api/question', methods=['POST'])
def ask_question():
    """
    Задать вопрос AI кулинару
    
    Request body:
        {
            "question": "Как правильно готовить яйцо?"
        }
    
    Response:
        {
            "success": true,
            "question": "Как правильно готовить яйцо?",
            "answer": "Ответ от AI..."
        }
    """
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    question = data.get('question', '')
    
    # Задаем вопрос через менеджер
    result = recipe_manager.ask_question(question)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@app.route('/api/substitute', methods=['POST'])
def get_substitute():
    """
    Получить замену для ингредиента
    
    Request body:
        {
            "ingredient": "масло"
        }
    
    Response:
        {
            "success": true,
            "ingredient": "масло",
            "substitutes": "Варианты замены..."
        }
    """
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    ingredient = data.get('ingredient', '')
    
    # Получаем замену через менеджер
    result = recipe_manager.get_substitute(ingredient)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """
    Добавить рецепт в избранное
    
    Request body:
        {
            "recipe": {
                "name": "Омлет",
                "ingredients": ["яйцо", "масло"],
                "instructions": "..."
            }
        }
    
    Response:
        {
            "success": true,
            "message": "Recipe added to favorites"
        }
    """
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    recipe = data.get('recipe', {})
    
    # Добавляем в избранное через менеджер
    result = recipe_manager.add_to_favorites(recipe)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """
    Получить все избранные рецепты
    
    Response:
        {
            "success": true,
            "favorites": [...],
            "count": 5
        }
    """
    
    result = recipe_manager.get_favorites()
    return jsonify(result), 200


# ============================================
# ERROR HANDLERS (Обработчики ошибок)
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Обработка ошибки 404 - не найдено"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка ошибки 500 - внутренняя ошибка сервера"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ============================================
# MAIN - Запуск сервера
# ============================================

if __name__ == '__main__':
    print("🍳 AI Culinary Assistant Backend запущен!")
    print("📍 http://localhost:5000")
    print("📚 API документация доступна по адресу /api/docs")
    
    # Запускаем сервер
    app.run(
        host='0.0.0.0',  # Доступен со всех адресов
        port=5000,       # Порт
        debug=True       # Режим отладки (автоперезагрузка при изменении кода)
    )
