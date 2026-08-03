import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from config import config

logger = logging.getLogger(__name__)

class GeminiService:
    """Сервис для безопасного взаимодействия с Google Gemini API."""

    def __init__(self):
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            # Модель для JSON-ответов (рецепты)
            self.json_model = genai.GenerativeModel(
                model_name=config.MODEL_NAME,
                generation_config={"response_mime_type": "application/json"}
            )
            # Модель для обычного текста (вопросы)
            self.text_model = genai.GenerativeModel(
                model_name=config.MODEL_NAME
            )
            logger.info("GeminiService успешно инициализирован.")
        except Exception as e:
            logger.critical(f"Ошибка инициализации GeminiService: {str(e)}")
            raise e

    def generate_recipes(self, ingredients: List[str]) -> Dict[str, Any]:
        if not ingredients or not isinstance(ingredients, list):
            return {
                "success": False,
                "error": "Список ингредиентов должен быть непустым массивом строк."
            }

        ingredients_clean = [str(item).strip() for item in ingredients if str(item).strip()]
        ingredients_str = ", ".join(ingredients_clean)

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

        try:
            logger.info(f"Запрос к Gemini API для ингредиентов: {ingredients_str}")
            response = self.json_model.generate_content(prompt)
            recipes_data = json.loads(response.text)
            
            return {
                "success": True,
                "data": recipes_data
            }
        except GoogleAPIError as e:
            logger.error(f"Ошибка Google Gemini API: {str(e)}")
            return {"success": False, "error": "Сервис ИИ временно недоступен."}
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {str(e)}")
            return {"success": False, "error": "Некорректный формат ответа от модели."}
        except Exception as e:
            logger.error(f"Непредвиденная ошибка в generate_recipes: {str(e)}")
            return {"success": False, "error": "Внутренняя ошибка сервера."}

    def answer_culinary_question(self, question: str) -> Dict[str, Any]:
        if not question or not isinstance(question, str):
            return {"success": False, "error": "Вопрос должен быть непустой строкой."}

        prompt = (
            "Ты опытный, вежливый кулинарный шеф-повар. "
            "Отвечай только на вопросы, связанные с кулинарией, продуктами и готовкой.\n"
            f"Вопрос пользователя: {question.strip()}"
        )

        try:
            response = self.text_model.generate_content(prompt)
            return {"success": True, "answer": response.text}
        except Exception as e:
            logger.error(f"Ошибка в answer_culinary_question: {str(e)}")
            return {"success": False, "error": "Не удалось получить ответ на вопрос."}

gemini_service = GeminiService()
