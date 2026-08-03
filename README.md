# 🍳 AI Culinary Assistant

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-18.0+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-8E75B2?style=for-the-badge&logo=googlecloud&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

Умный кулинарный помощник на базе **Google Gemini API**, который помогает находить рецепты по имеющимся ингредиентам и отвечает на кулинарные вопросы. Приложение состоит из Flask RESTful API бэкенда и современно оформленного React фронтенда.

---

## 🌟 Основные возможности

- 🥦 **Генерация рецептов по ингредиентам:** Введите список продуктов, которые есть у вас дома, и AI предложит пошаговые рецепты.
- ⏱ **Умная структуризация:** Каждый рецепт содержит уровень сложности, время приготовления, список ингредиентов и пронумерованную инструкцию.
- 👨‍🍳 **Кулинарный консультант:** Возможность задать свободный вопрос о готовке, замене ингредиентов или технологиях обработки продуктов.
- 🛡 **Устойчивость к ошибкам:** Бэкенд строго валидирует входящие данные и возвращает детерминированный JSON.

---

## 🏗 Архитектура и стек технологий

Проект построен по принципу разделения ответственности (**Separation of Concerns**):

### **Backend**
- **Language:** Python 3.10+
- **Framework:** Flask (REST API)
- **AI Integration:** Google Gemini API (`google-generativeai`)
- **CORS Management:** `Flask-CORS`
- **Validation & Error Handling:** Кастомные обработчики HTTP-ошибок (400, 422, 500)

### **Frontend**
- **Library:** React 18
- **Styling:** CSS3 (Flexbox & CSS Grid, адаптивный интерфейс)
- **HTTP Client:** Fetch API

---

## 📁 Структура проекта

```text
ai-culinary-assistant/
│
├── backend/
│   ├── app.py                  # Главный точку входа Flask API и эндпоинты
│   ├── gemini_service.py       # Модуль интеграции с Gemini API
│   ├── config.py               # Конфигурация приложения и переменные окружения
│   └── requirements.txt        # Зависимости Python
│
├── frontend/
│   ├── public/                 # Статические файлы
│   └── src/
│       ├── components/
│       │   ├── RecipeList.js   # Отображение карточек рецептов
│       │   └── ...             # Другие UI компоненты
│       ├── App.js              # Главный компонент React
│       └── App.css             # Стили приложения
│
└── README.md                   # Документация проекта
