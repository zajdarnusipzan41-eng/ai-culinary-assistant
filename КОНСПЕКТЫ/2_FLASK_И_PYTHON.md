# 🐍 КОНСПЕКТ 2: Flask и как это работает

## 📚 Что такое Flask?

**Flask** = фреймворк (набор готовых инструментов) для создания веб-серверов на Python.

Думайте о нём как о **конструкторе LEGO**:
- Без Flask: нужно строить всё с нуля
- С Flask: уже есть готовые кирпичики, нужно их собрать

---

## 🚀 Основные концепции Flask

### 1️⃣ **Application (Приложение)**

```python
from flask import Flask

# Создаём Flask приложение
app = Flask(__name__)

# __name__ = имя текущего модуля Python
# Это нужно Flask для поиска файлов (templates, static и т.д.)
```

**Что это делает:**
- Создаёт объект приложения
- Регистрирует всё, что будет дальше

---

### 2️⃣ **Routes (Маршруты)**

Маршрут = URL адрес + функция, которая его обрабатывает

```python
@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    # Эта функция вызывается, когда приходит запрос на /api/recipes
    return {"message": "Рецепты здесь"}
```

**Декоратор `@app.route()`:**
- `'/api/recipes'` = путь (URL)
- `methods=['POST']` = какой метод HTTP принимаем

---

### 3️⃣ **HTTP методы**

| Метод | Что делает | Пример |
|-------|-----------|--------|
| **GET** | Получить данные | Запрос рецептов |
| **POST** | Отправить данные | Отправка ингредиентов |
| **PUT** | Обновить данные | Обновить рецепт |
| **DELETE** | Удалить данные | Удалить рецепт |

**В нашем проекте используем:**
- `GET /api/favorites` - получить избранные
- `POST /api/recipes` - отправить ингредиенты

---

## 🔄 Жизненный цикл запроса

```
1. Клиент (Frontend) отправляет запрос
   POST http://localhost:5000/api/recipes
   Body: { "ingredients": ["яйцо", "масло"] }
                        ↓
2. Flask ловит запрос на маршруте /api/recipes
                        ↓
3. Вызывает функцию get_recipes()
                        ↓
4. Функция обрабатывает данные
   - Читает ингредиенты
   - Вызывает AI
   - Генерирует рецепты
                        ↓
5. Возвращает ответ
   { "success": true, "recipes": "..." }
                        ↓
6. Flask отправляет ответ клиенту
                        ↓
7. Frontend получает ответ и показывает пользователю
```

---

## 📥 Как получить данные из запроса?

### Способ 1: JSON данные (POST)

```python
from flask import request

@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    # Получаем JSON из тела запроса
    data = request.get_json()
    
    # Вытаскиваем поля
    ingredients = data.get('ingredients', [])
    
    # Используем данные
    print(ingredients)  # ['яйцо', 'масло']
    
    return {"success": True}
```

**Запрос от клиента:**
```javascript
fetch('/api/recipes', {
    method: 'POST',
    body: JSON.stringify({
        ingredients: ['яйцо', 'масло']
    })
})
```

---

### Способ 2: Query параметры (GET)

```python
@app.route('/api/search', methods=['GET'])
def search():
    # Получаем параметры из URL
    query = request.args.get('q', '')
    
    # Используем данные
    print(query)  # 'рецепт борща'
    
    return {"results": [...]}
```

**Запрос от клиента:**
```javascript
fetch('/api/search?q=рецепт борща')
```

---

## 📤 Как отправить ответ?

### Способ 1: Словарь → JSON

```python
@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    # Python словарь
    result = {
        "success": True,
        "recipes": "Омлет, блины..."
    }
    
    # Flask автоматически преобразует в JSON
    return result
```

**Что получит клиент:**
```json
{
    "success": true,
    "recipes": "Омлет, блины..."
}
```

---

### Способ 2: jsonify + статус код

```python
from flask import jsonify

@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    result = {
        "success": True,
        "recipes": "Омлет, блины..."
    }
    
    # Явно преобразуем в JSON и устанавливаем статус код
    return jsonify(result), 200
```

**Статус коды:**
- `200` = OK, всё хорошо
- `400` = Bad Request, ошибка в запросе
- `404` = Not Found, ресурс не найден
- `500` = Server Error, ошибка на сервере

---

## 🛡️ CORS (Cross-Origin Resource Sharing)

**Проблема:**
- Frontend работает на `http://localhost:3000`
- Backend работает на `http://localhost:5000`
- Браузер не разрешает запросы между разными портами (разные origins)

**Решение: CORS**

```python
from flask_cors import CORS

# Разрешаем запросы с фронтенда
CORS(app, origins=["http://localhost:3000"])
```

**Что это делает:**
- Добавляет специальные HTTP заголовки
- Браузер видит эти заголовки и разрешает запрос

---

## 🎯 Полный пример маршрута

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    """
    Получить рецепты по ингредиентам
    
    Request:
        POST /api/recipes
        {
            "ingredients": ["яйцо", "масло"]
        }
    
    Response:
        {
            "success": true,
            "recipes": "Омлет..."
        }
    """
    
    # Шаг 1: Получаем данные
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    # Шаг 2: Валидация (проверка)
    if not ingredients:
        return jsonify({
            "success": False,
            "error": "Укажите ингредиенты"
        }), 400
    
    # Шаг 3: Обработка
    recipes = generate_recipes_from_ai(ingredients)
    
    # Шаг 4: Ответ
    return jsonify({
        "success": True,
        "ingredients": ingredients,
        "recipes": recipes
    }), 200
```

---

## 📊 Request & Response структура

```
┌─────────────────────────────────────┐
│         REQUEST (от клиента)         │
├─────────────────────────────────────┤
│ HTTP метод: POST                    │
│ URL: http://localhost:5000/api/...  │
│ Headers: {                          │
│   "Content-Type": "application/json"│
│ }                                   │
│ Body: {                             │
│   "ingredients": ["яйцо"]           │
│ }                                   │
└─────────────────────────────────────┘
              ↓ Flask обрабатывает ↓
┌─────────────────────────────────────┐
│        RESPONSE (сервер отправляет)  │
├─────────────────────────────────────┤
│ Status Code: 200                    │
│ Headers: {                          │
│   "Content-Type": "application/json"│
│ }                                   │
│ Body: {                             │
│   "success": true,                  │
│   "recipes": "Омлет..."             │
│ }                                   │
└─────────────────────────────────────┘
```

---

## ⚙️ Как запустить Flask сервер?

### Шаг 1: Установить зависимости
```bash
cd backend
pip install -r requirements.txt
```

### Шаг 2: Создать .env файл
```bash
cp .env.example .env
# Добавьте GEMINI_API_KEY в .env
```

### Шаг 3: Запустить сервер
```bash
python app.py
```

**Результат:**
```
🍳 AI Culinary Assistant Backend запущен!
📍 http://localhost:5000
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

## 🧪 Как проверить Flask?

### Метод 1: Через браузер
```
Откройте: http://localhost:5000/api/health
Должно быть: {"status": "ok", "message": "Server is running"}
```

### Метод 2: Через curl (терминал)
```bash
# GET запрос
curl http://localhost:5000/api/health

# POST запрос
curl -X POST http://localhost:5000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"ingredients": ["яйцо", "масло"]}'
```

### Метод 3: Через Postman (приложение)
1. Скачайте Postman
2. Создайте новый POST запрос
3. URL: `http://localhost:5000/api/recipes`
4. Body (JSON):
```json
{
    "ingredients": ["яйцо", "масло"]
}
```
5. Отправьте запрос

---

## 💡 Ключевые концепции

| Концепция | Что это |
|-----------|--------|
| **Route** | URL адрес + функция |
| **Endpoint** | Один маршрут (например: POST /api/recipes) |
| **Request** | Запрос от клиента |
| **Response** | Ответ сервера |
| **JSON** | Формат данных |
| **CORS** | Разрешение на кросс-доменные запросы |
| **HTTP метод** | GET, POST, PUT, DELETE и т.д. |
| **Status Code** | Код результата (200, 400, 500 и т.д.) |

---

## 🔗 Как это работает в нашем проекте?

```
Frontend (React)
      ↓
Пользователь вводит: ["яйцо", "масло"]
      ↓
JavaScript отправляет POST запрос
      ↓
app.py получает на маршруте /api/recipes
      ↓
Функция get_recipes() обрабатывает
      ↓
recipes.py вызывает RecipeManager
      ↓
gemini_service.py вызывает Google Gemini
      ↓
Google возвращает рецепты
      ↓
app.py отправляет JSON ответ
      ↓
Frontend получает и показывает пользователю
```

---

## ✅ Запомните

1. **Flask** = фреймворк для создания веб-серверов на Python
2. **Routes** = маршруты (URL + функция)
3. **HTTP методы** = GET (получить), POST (отправить), PUT, DELETE
4. **JSON** = формат данных для передачи
5. **CORS** = разрешение на запросы с других доменов
6. **Status codes** = коды результата (200 = OK, 400 = ошибка, 500 = сервер сломался)

Дальше: Google Gemini API! 🚀
