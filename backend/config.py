# ============================================
# КОНФИГ - Настройки приложения
# ============================================

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    """Основные настройки приложения"""
    
    # Flask настройки
    DEBUG = True
    TESTING = False
    
    # CORS (разрешаем запросы с фронтенда)
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5000"]
    
    # Google Gemini API key
    # Получить можно здесь: https://aistudio.google.com/app/apikey
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
    
    # Параметры AI модели
    MODEL_NAME = "gemini-pro"
    TEMPERATURE = 0.7  # 0 = точный, 1 = творческий
    MAX_OUTPUT_TOKENS = 1000

# Переключатель конфигураций (для разработки/production)
config = Config()
