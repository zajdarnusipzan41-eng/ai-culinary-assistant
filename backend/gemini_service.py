# ============================================
# GEMINI SERVICE - Интеграция с Google AI
# ============================================

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        # Настройка модели
        self.model = genai.GenerativeModel(
            model_name=config.MODEL_NAME,
            generation_config={"response_mime_type": "application/json"}
        )

    def generate_recipes(self, ingredients: list) -> dict:
        if not ingredients or not isinstance(ingredients, list):
            raise ValueError("Ingredients must be a non-empty list.")

        ingredients_str = ", ".join(ingredients)
        prompt = f"""
        You are a professional chef. Given these ingredients: {ingredients_str}.
        Return a JSON array of 2 recipes in this structure:
        [
          {{
            "title": "String",
            "time": "String",
            "difficulty": "Easy|Medium|Hard",
            "steps": ["Step 1", "Step 2"]
          }}
        ]
        """
        try:
            response = self.model.generate_content(prompt)
            return {"success": True, "data": response.text}
        except GoogleAPIError as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return {"success": False, "error": "AI Service currently unavailable."}
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return {"success": False, "error": "An internal error occurred."}
