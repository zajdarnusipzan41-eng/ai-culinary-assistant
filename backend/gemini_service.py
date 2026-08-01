# ============================================
# GEMINI SERVICE - Интеграция с Google AI
# ============================================

import google.generativeai as genai
from config import config

class GeminiService:
    """Сервис для работы с Google Gemini API"""
    
    def __init__(self):
        """Инициализация сервиса"""
        # Устанавливаем API key
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Создаем модель
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def generate_recipes(self, ingredients: list) -> str:
        """
        Генерирует рецепты по списку ингредиентов
        
        Args:
            ingredients (list): Список ингредиентов
                Пример: ["яйцо", "масло", "мука"]
        
        Returns:
            str: Сгенерированные рецепты
        """
        
        # Формируем промпт (инструкция для AI)
        ingredients_str = ", ".join(ingredients)
        prompt = f"""
        Ты профессиональный шеф-повар. 
        Дан список ингредиентов: {ingredients_str}
        
        Предложи 2-3 рецепта, которые можно приготовить из этих ингредиентов.
        Для каждого рецепта указывай:
        1. Название
        2. Время приготовления
        3. Пошаговые инструкции
        4. Сложность (легко/средне/сложно)
        """
        
        # Отправляем запрос к AI и получаем ответ
        response = self.model.generate_content(prompt)
        
        return response.text
    
    def answer_culinary_question(self, question: str) -> str:
        """
        Отвечает на вопросы о кулинарии
        
        Args:
            question (str): Вопрос о кулинарии
        
        Returns:
            str: Ответ от AI
        """
        
        prompt = f"""
        Ты опытный кулинар и эксперт по кухне.
        Ответь на вопрос пользователя:
        
        {question}
        
        Дай практичный, понятный ответ.
        """
        
        response = self.model.generate_content(prompt)
        
        return response.text
    
    def suggest_substitute(self, ingredient: str) -> str:
        """
        Предлагает замену для ингредиента
        
        Args:
            ingredient (str): Ингредиент для замены
        
        Returns:
            str: Варианты замены
        """
        
        prompt = f"""
        Предложи 3-4 замены для ингредиента: {ingredient}
        
        Для каждой замены указывай:
        1. Название ингредиента
        2. Как его использовать вместо оригинального
        3. Как это повлияет на вкус блюда
        """
        
        response = self.model.generate_content(prompt)
        
        return response.text

# Создаем глобальный объект сервиса
gemini_service = GeminiService()
