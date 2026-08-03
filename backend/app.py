import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_service import gemini_service
from config import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Безопасная настройка CORS
CORS(app, origins=config.CORS_ORIGINS)


@app.route('/api/health', methods=['GET'])
def health():
    """Проверка работоспособности сервиса (Health Check)."""
    return jsonify({
        "status": "healthy",
        "service": "AI Culinary Assistant API"
    }), 200


@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    """
    Генерация рецептов по списку ингредиентов.
    Expects JSON: { "ingredients": ["яйцо", "мука"] }
    """
    data = request.get_json(silent=True)
    
    if not data or 'ingredients' not in data:
        return jsonify({
            "success": False,
            "error": "Необходимо передать поле 'ingredients' в JSON формате."
        }), 400

    ingredients = data.get('ingredients')
    
    if not isinstance(ingredients, list) or len(ingredients) == 0:
        return jsonify({
            "success": False,
            "error": "Поле 'ingredients' должно быть непустым массивом."
        }), 422

    # Вызов сервиса Gemini
    result = gemini_service.generate_recipes(ingredients)
    
    status_code = 200 if result.get('success') else 500
    return jsonify(result), status_code


@app.route('/api/question', methods=['POST'])
def ask_question():
    """
    Задать кулинарный вопрос AI.
    Expects JSON: { "question": "Текст вопроса" }
    """
    data = request.get_json(silent=True)
    
    if not data or 'question' not in data:
        return jsonify({
            "success": False,
            "error": "Необходимо передать поле 'question' в JSON формате."
        }), 400

    question = data.get('question')
    
    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "success": False,
            "error": "Вопрос не может быть пустым."
        }), 422

    result = gemini_service.answer_culinary_question(question)
    
    status_code = 200 if result.get('success') else 500
    return jsonify(result), status_code


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Запрашиваемый эндпоинт не найден."
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Внутренняя ошибка сервера: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Внутренняя ошибка сервера. Попробуйте позже."
    }), 500


if __name__ == '__main__':
    logger.info("🍳 Запуск AI Culinary Assistant Backend...")
    # debug берётся из конфигурации, а не зашит жёстко
    app.run(
        host=getattr(config, 'HOST', '127.0.0.1'),
        port=getattr(config, 'PORT', 5000),
        debug=getattr(config, 'DEBUG', False)
    )
