# 🌐 КОНСПЕКТ 5: HTTP запросы и Fetch API

## 📚 Что такое HTTP запросы?

**HTTP** = протокол (язык) общения между клиентом (браузер) и сервером (backend).

**Простой пример:**
```
Frontend (браузер)                Backend (сервер)
      ↓ HTTP запрос ↓
   "Дай рецепты для яйца"
      ↓ ↓ ↓
      Backend обрабатывает
      ↓ ↓ ↓
      ← HTTP ответ ←
   "Омлет, блины, ..."
```

---

## 📤 Как отправить запрос из Frontend?

### Способ 1: Старый способ (XMLHttpRequest)

```javascript
// ❌ Старый способ (не используем)
var xhr = new XMLHttpRequest();
xhr.open('POST', '/api/recipes');
xhr.send(JSON.stringify({ingredients: ['яйцо']}));
```

### Способ 2: Современный способ (Fetch API) ✅

```javascript
// ✅ Новый способ (используем этот!)
fetch('/api/recipes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    ingredients: ['яйцо', 'масло']
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Ошибка:', error));
```

---

## 🔍 Разбор Fetch API

### Структура запроса:

```javascript
fetch(URL, {
  method: 'POST',           // HTTP метод
  headers: {                // Заголовки
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({    // Тело запроса (JSON)
    ingredients: ['яйцо']
  })
})
```

### Параметры:

| Параметр | Значение | Пример |
|----------|----------|--------|
| **URL** | Адрес endpoint | '/api/recipes' |
| **method** | HTTP метод | 'GET', 'POST', 'PUT', 'DELETE' |
| **headers** | Информация о запросе | { 'Content-Type': 'application/json' } |
| **body** | Данные в запросе | JSON.stringify({...}) |

---

## 📝 Примеры разных HTTP методов

### 1️⃣ GET - Получить данные

```javascript
// Получить избранные рецепты
fetch('/api/favorites', {
  method: 'GET'
})
.then(response => response.json())
.then(data => {
  console.log('Избранные:', data.favorites);
})
```

**Когда использовать:** Получение данных со сервера

---

### 2️⃣ POST - Отправить данные

```javascript
// Отправить ингредиенты и получить рецепты
fetch('/api/recipes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    ingredients: ['яйцо', 'масло', 'мука']
  })
})
.then(response => response.json())
.then(data => {
  console.log('Рецепты:', data.recipes);
})
```

**Когда использовать:** Создание новых данных, отправка информации

---

### 3️⃣ PUT - Обновить данные

```javascript
// Обновить рецепт
fetch('/api/recipes/123', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Омлет',
    time: '10 минут'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Обновлено:', data);
})
```

**Когда использовать:** Изменение существующих данных

---

### 4️⃣ DELETE - Удалить данные

```javascript
// Удалить рецепт
fetch('/api/recipes/123', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => {
  console.log('Удалено:', data);
})
```

**Когда использовать:** Удаление данных

---

## 🔄 Жизненный цикл Fetch запроса

```
1. Отправка запроса
   fetch('/api/recipes', {...})
                    ↓
2. Браузер отправляет HTTP запрос на сервер
                    ↓
3. Сервер получает и обрабатывает
                    ↓
4. Сервер отправляет ответ
                    ↓
5. Браузер получает ответ
   response.json()  ← Преобразуем в JavaScript объект
                    ↓
6. Обработка данных в коде
   .then(data => console.log(data))
```

---

## 📋 Обработка ответа

### Шаг 1: Получить ответ

```javascript
fetch('/api/recipes', {...})
  .then(response => {
    console.log(response);  // Response object
    console.log(response.status);  // 200, 400, 500 и т.д.
    console.log(response.ok);  // true если 200-299
    return response.json();  // Преобразуем в JSON
  })
```

### Шаг 2: Использовать данные

```javascript
  .then(data => {
    console.log(data);  // JavaScript объект
    // data = {
    //   success: true,
    //   recipes: "Омлет, блины, ..."
    // }
  })
```

### Шаг 3: Обработать ошибки

```javascript
  .catch(error => {
    console.error('Ошибка:', error);
    // Показать пользователю сообщение об ошибке
  })
```

---

## 🚨 Обработка ошибок

### Ошибки при сетевом запросе

```javascript
fetch('/api/recipes', {...})
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Успех!', data.recipes);
    } else {
      console.error('Ошибка от сервера:', data.error);
    }
  })
  .catch(error => {
    console.error('Ошибка сети:', error);
    // Сервер не ответил, нет интернета и т.д.
  })
```

### Проверка статус кода

```javascript
fetch('/api/recipes', {...})
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP ошибка! Статус: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log('Успех:', data))
  .catch(error => console.error('Ошибка:', error))
```

---

## ⚡ Async/Await - современный синтаксис

**Старый способ (Promises):**
```javascript
fetch('/api/recipes', {...})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error))
```

**Новый способ (Async/Await):** ✅

```javascript
async function getRecipes() {
  try {
    const response = await fetch('/api/recipes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ingredients: ['яйцо'] })
    });

    if (!response.ok) {
      throw new Error('Ошибка при получении рецептов');
    }

    const data = await response.json();
    console.log('Рецепты:', data.recipes);
    return data;
  } catch (error) {
    console.error('Ошибка:', error);
  }
}

// Вызываем функцию
getRecipes();
```

**Преимущества:**
- Легче читать
- Похоже на синхронный код
- Проще обрабатывать ошибки

---

## 💻 Полный пример в React компоненте

```javascript
import React from 'react';

function RecipeForm() {
  const [ingredients, setIngredients] = React.useState([]);
  const [recipes, setRecipes] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  // Функция для отправки запроса
  const handleSearch = async () => {
    // Очищаем ошибки
    setError(null);
    setLoading(true);

    try {
      // Отправляем POST запрос
      const response = await fetch('/api/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ingredients: ingredients
        })
      });

      // Проверяем статус ответа
      if (!response.ok) {
        throw new Error(`HTTP ошибка! Статус: ${response.status}`);
      }

      // Преобразуем ответ в JSON
      const data = await response.json();

      // Проверяем успешность операции
      if (data.success) {
        setRecipes(data.recipes);
      } else {
        setError(data.error || 'Неизвестная ошибка');
      }
    } catch (error) {
      console.error('Ошибка:', error);
      setError('Ошибка при получении рецептов. Проверьте подключение.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Поиск рецептов</h2>
      
      {/* Форма */}
      <input
        type="text"
        placeholder="Введите ингредиенты"
        onChange={(e) => setIngredients(e.target.value.split(','))}
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Ищу...' : 'Поиск'}
      </button>

      {/* Показываем ошибку */}
      {error && <p style={{color: 'red'}}>{error}</p>}

      {/* Показываем результат */}
      {recipes && <p>{recipes}</p>}

      {/* Показываем загрузку */}
      {loading && <p>⏳ Загружаю...</p>}
    </div>
  );
}

export default RecipeForm;
```

---

## 🎯 Запросы в нашем приложении

### 1️⃣ Получить рецепты

```javascript
async function searchRecipes(ingredients) {
  const response = await fetch('/api/recipes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ingredients })
  });
  return await response.json();
}

// Использование
const result = await searchRecipes(['яйцо', 'масло']);
console.log(result.recipes);
```

---

### 2️⃣ Задать вопрос AI

```javascript
async function askQuestion(question) {
  const response = await fetch('/api/question', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  return await response.json();
}

// Использование
const result = await askQuestion('Как готовить яйцо?');
console.log(result.answer);
```

---

### 3️⃣ Получить избранные рецепты

```javascript
async function getFavorites() {
  const response = await fetch('/api/favorites', {
    method: 'GET'
  });
  return await response.json();
}

// Использование
const result = await getFavorites();
console.log(result.favorites);
```

---

### 4️⃣ Добавить рецепт в избранное

```javascript
async function addFavorite(recipe) {
  const response = await fetch('/api/favorites', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipe })
  });
  return await response.json();
}

// Использование
await addFavorite({ name: 'Омлет', time: '5 минут' });
```

---

## 🔗 Frontend ↔ Backend общение

```
┌──────────────────────────────────────────────────────────────┐
│                      ПОЛЬЗОВАТЕЛЬ                            │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│                                                              │
│  RecipeForm компонент:                                       │
│  - Пользователь вводит: "яйцо, масло"                       │
│  - onClick: handleSearch()                                   │
│  - Вызывает fetch('/api/recipes', {...})                    │
└──────────────────────────────────────────────────────────────┘
                    ↓ HTTP POST запрос ↓
           {ingredients: ['яйцо', 'масло']}
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask)                          │
│                                                              │
│  app.py маршрут: POST /api/recipes                          │
│  - Получает ингредиенты                                     │
│  - Вызывает recipes.py                                       │
│  - Вызывает gemini_service.py                               │
│  - Gemini генерирует рецепты                                │
│  - Возвращает JSON ответ                                    │
└──────────────────────────────────────────────────────────────┘
                    ↓ HTTP ответ (200 OK) ↓
      {success: true, recipes: "Омлет..."}
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│                                                              │
│  .then(data => setRecipes(data.recipes))                    │
│  RecipeList компонент:                                       │
│  - Показывает рецепты пользователю                          │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                      ПОЛЬЗОВАТЕЛЬ                            │
│              Видит рецепты на экране! 🎉                     │
└──────────────────────────────────────────────────────────────┘
```

---

## ✅ Запомните

1. **Fetch** = современный способ отправлять запросы
2. **HTTP методы:** GET (получить), POST (отправить), PUT (обновить), DELETE (удалить)
3. **Headers** = информация о запросе
4. **Body** = данные в запросе (JSON)
5. **Response** = ответ от сервера
6. **Async/Await** = современный синтаксис для работы с запросами
7. **Обработка ошибок** = важна!

Дальше: **State и Props в React!** 🚀
