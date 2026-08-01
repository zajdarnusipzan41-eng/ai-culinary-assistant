# ============================================
# RECIPES - Логика работы с рецептами
# ============================================

from gemini_service import gemini_service

class RecipeManager:
    """Менеджер для работы с рецептами"""
    
    def __init__(self):
        """Инициализация менеджера"""
        # Хранилище любимых рецептов в памяти
        # В реальном приложении это была бы база данных (MongoDB, PostgreSQL)
        self.favorites = []
    
    def get_recipes_by_ingredients(self, ingredients: list) -> dict:
        """
        Получает рецепты на основе ингредиентов
        
        Args:
            ingredients (list): Список ингредиентов
        
        Returns:
            dict: Словарь с рецептами и статусом
        """
        
        if not ingredients:
            return {
                "success": False,
                "error": "Пожалуйста, укажите хотя бы один ингредиент"
            }
        
        try:
            # Запрашиваем AI для генерации рецептов
            recipes_text = gemini_service.generate_recipes(ingredients)
            
            return {
                "success": True,
                "ingredients": ingredients,
                "recipes": recipes_text
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при генерации рецептов: {str(e)}"
            }
    
    def ask_question(self, question: str) -> dict:
        """
        Отвечает на вопрос о кулинарии
        
        Args:
            question (str): Вопрос
        
        Returns:
            dict: Ответ и статус
        """
        
        if not question:
            return {
                "success": False,
                "error": "Пожалуйста, введите вопрос"
            }
        
        try:
            answer = gemini_service.answer_culinary_question(question)
            
            return {
                "success": True,
                "question": question,
                "answer": answer
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при ответе на вопрос: {str(e)}"
            }
    
    def get_substitute(self, ingredient: str) -> dict:
        """
        Предлагает замену для ингредиента
        
        Args:
            ingredient (str): Ингредиент для замены
        
        Returns:
            dict: Варианты замены и статус
        """
        
        if not ingredient:
            return {
                "success": False,
                "error": "Пожалуйста, укажите ингредиент"
            }
        
        try:
            substitutes = gemini_service.suggest_substitute(ingredient)
            
            return {
                "success": True,
                "ingredient": ingredient,
                "substitutes": substitutes
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Ошибка при поиске замены: {str(e)}"
            }
    
    def add_to_favorites(self, recipe: dict) -> dict:
        """
        Добавляет рецепт в избранное
        
        Args:
            recipe (dict): Рецепт для добавления
        
        Returns:
            dict: Статус добавления
        """
        
        if not recipe:
            return {
                "success": False,
                "error": "Рецепт не может быть пустым"
            }
        
        self.favorites.append(recipe)
        
        return {
            "success": True,
            "message": "Рецепт добавлен в избранное",
            "total_favorites": len(self.favorites)
        }
    
    def get_favorites(self) -> dict:
        """
        Получает все избранные рецепты
        
        Returns:
            dict: Список избранных рецептов
        """
        
        return {
            "success": True,
            "favorites": self.favorites,
            "count": len(self.favorites)
        }

# Создаем глобальный объект менеджера
recipe_manager = RecipeManager()
