import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError, RetryError
from config import config

# Настройка профессионального логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class GeminiService:
    """Сервис для безопасного взаимодействия с Google Gemini API."""

    def __init__(self):
        """Инициализация конфигурации Gemini API."""
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            # Настраиваем модель на принудительный возврат JSON
            self.model = genai.GenerativeModel(
                model_name=config.MODEL_NAME,
                generation_config={"response_mime_type": "application/json"}
            )
            logger.info("GeminiService успешно инициализирован.")
        except Exception as e:
            logger.critical(f"Ошибка инициализации GeminiService: {str(e)}")
            raise e

    def generate_recipes(self, ingredients: List[str]) -> Dict[str, Any]:
        """
        Генерирует рецепты по списку ингредиентов в формате JSON.

        Args:
            ingredients (List[str]): Список названий ингредиентов.

        Returns:
            Dict[str, Any]: Словарь со статусом выполнения и результатом/ошибкой.
        """
        # 1. Валидация входных данных
        if not ingredients or not isinstance(ingredients, list):
            logger.warning("Попытка вызова generate_recipes с пустым или некорректным списком.")
            return {
                "success": False,
                "error": "Список ингредиентов должен быть непустым массивом строк."
            }

        ingredients_clean = [str(item).strip() for item in ingredients if str(item).strip()]
        ingredients_str = ", ".join(ingredients_clean)

        # 2. Промпт с чётким контрактом JSON
        prompt = f"""
        Ты профессиональный шеф-повар.
        Ингредиенты: {ingredients_str}.
        
        Сгенерируй 2-3 рецепта и верни их строго в формате JSON по следующей схеме:
        [
          {{
            "title": "Название блюда",
            "cooking_time": "Время (например, 20 мин)",
            "difficulty": "Легко | Средне | Сложно",
            "ingredients_used": ["ингредиент 1", "ингредиент 2"],
            "steps": ["Шаг 1", "Шаг 2"]
          }}
        ]
        """

        # 3. Безопасный вызов API с обработкой исключений
        try:
            logger.info(f"Запрос к Gemini API для ингредиентов: {ingredients_str}")
            response = self.model.generate_content(prompt)

            # Парсим гарантированный JSON от модели
            recipes_data = json.loads(response.text)
            
            return {
                "success": True,
                "data": recipes_data
            }

        except GoogleAPIError as e:
            logger.error(f"Ошибка Google Gemini API: {str(e)}")
            return {
                "success": False,
                "error": "Сервис ИИ временно недоступен. Попробуйте позже."
            }
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON ответа: {str(e)}")
            return {
                "success": False,
                "error": "Некорректный формат ответа от модели."
            }
        except Exception as e:
            logger.error(f"Непредвиденная ошибка в GeminiService: {str(e)}")
            return {
                "success": False,
                "error": "Внутренняя ошибка при обработке запроса."
            }

    def answer_culinary_question(self, question: str) -> Dict[str, Any]:
        """Отвечает на кулинарные вопросы с обработкой ошибок."""
        if not question or not isinstance(question, str):
            return {"success": False, "error": "Вопрос должен быть непустой строкой."}

        prompt = f"Ты опытный шеф-повар. Ответь кратко и понятно на вопрос: {question.strip()}"

        try:
            # Для обычного чата переключаем или создаем стандартный текстовый запрос
            text_model = genai.GenerativeModel(config.MODEL_NAME)
            response = text_model.generate_content(prompt)
            return {"success": True, "answer": response.text}
        except Exception as e:
            logger.error(f"Ошибка в answer_culinary_question: {str(e)}")
            return {"success": False, "error": "Не удалось получить ответ на вопрос."}


# Singleton экземпляр
gemini_service = GeminiService()
