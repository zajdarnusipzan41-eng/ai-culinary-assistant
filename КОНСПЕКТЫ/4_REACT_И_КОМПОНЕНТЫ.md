# ⚛️ КОНСПЕКТ 4: React и компоненты

## 📚 Что такое React?

**React** = библиотека (набор инструментов) для создания интерфейсов на JavaScript.

**Простое объяснение:**
- Без React: нужно вручную менять HTML элементы
- С React: описываете, как должно выглядеть, а React сам обновляет страницу

---

## 🧩 Что такое Компонент?

**Компонент** = переиспользуемый кусок интерфейса (UI).

### Пример из реальной жизни:

```
┌─────────────────────────────────┐
│         ПРИЛОЖЕНИЕ              │
├─────────────────────────────────┤
│                                 │
│  ┌──────────────────────────┐   │
│  │    Header Компонент      │   │
│  │  (логотип, меню)         │   │
│  └──────────────────────────┘   │
│                                 │
│  ┌──────────────────────────┐   │
│  │   RecipeForm Компонент   │   │
│  │  (форма ввода)           │   │
│  └──────────────────────────┘   │
│                                 │
│  ┌──────────────────────────┐   │
│  │  RecipeList Компонент    │   │
│  │  (список рецептов)       │   │
│  └──────────────────────────┘   │
│                                 │
│  ┌──────────────────────────┐   │
│  │   Chat Компонент         │   │
│  │  (чат с AI)              │   │
│  └──────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

Каждый компонент = отдельный файл с логикой + внешний вид

---

## 💻 Синтаксис React (JSX)

React использует **JSX** = смесь JavaScript + HTML

### Пример 1: Простой компонент

```jsx
// RecipeForm.js
import React from 'react';

// Компонент = функция, которая возвращает HTML-подобный код
function RecipeForm() {
  return (
    <div>
      <h1>Введите ингредиенты</h1>
      <input type="text" placeholder="Ингредиент" />
      <button>Поиск рецепта</button>
    </div>
  );
}

export default RecipeForm;
```

**Что это делает:**
- Функция `RecipeForm()` возвращает HTML элементы
- Это HTML-подобный синтаксис = JSX
- Компонент можно использовать в других файлах

### Пример 2: Использование компонента

```jsx
// App.js
import RecipeForm from './components/RecipeForm';

function App() {
  return (
    <div>
      <h1>🍳 AI Culinary Assistant</h1>
      <RecipeForm />  {/* Используем компонент как тег */}
    </div>
  );
}

export default App;
```

---

## 🔄 Жизненный цикл компонента

```
1. Создание (Mounting)
   Компонент впервые добавляется на страницу
                    ↓
2. Отображение (Rendering)
   React рендерит HTML в браузер
                    ↓
3. Обновление (Updating)
   Данные меняются → React обновляет страницу
                    ↓
4. Удаление (Unmounting)
   Компонент удаляется со страницы
```

---

## 📂 Структура нашего Frontend

```
frontend/
├── src/
│   ├── App.js              # 🌟 Главный компонент
│   ├── App.css             # Стили для App
│   ├── index.js            # Точка входа
│   └── components/
│       ├── RecipeForm.js   # Форма ввода ингредиентов
│       ├── RecipeList.js   # Список рецептов
│       └── Chat.js         # Чат с AI
│
├── public/
│   └── index.html          # HTML файл (основа для всего)
│
├── package.json            # Зависимости и скрипты
└── .gitignore             # Что не загружать на GitHub
```

---

## 🎨 Компоненты нашего приложения

### 1️⃣ **RecipeForm** - Форма ввода ингредиентов

```jsx
function RecipeForm({ onSearch }) {
  const [ingredients, setIngredients] = React.useState([]);
  const [input, setInput] = React.useState('');

  const handleAddIngredient = () => {
    if (input.trim()) {
      setIngredients([...ingredients, input]);
      setInput('');
    }
  };

  const handleSearch = () => {
    if (ingredients.length > 0) {
      onSearch(ingredients);
    }
  };

  return (
    <div className="form-container">
      <h2>Введите ингредиенты</h2>
      <input
        type="text"
        placeholder="Например: яйцо, масло"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleAddIngredient}>Добавить</button>
      
      <div className="ingredients-list">
        {ingredients.map((ing, index) => (
          <span key={index} className="ingredient-tag">
            {ing} ✕
          </span>
        ))}
      </div>
      
      <button onClick={handleSearch} className="search-btn">
        🔍 Найти рецепты
      </button>
    </div>
  );
}
```

**Что делает:**
- Форма для ввода ингредиентов
- Кнопка для добавления ингредиента
- Отображение списка добавленных ингредиентов
- Отправка на поиск

---

### 2️⃣ **RecipeList** - Список рецептов

```jsx
function RecipeList({ recipes }) {
  return (
    <div className="recipes-container">
      <h2>Найденные рецепты</h2>
      {recipes ? (
        <div className="recipe">
          <p>{recipes}</p>
        </div>
      ) : (
        <p>Введите ингредиенты для поиска рецептов</p>
      )}
    </div>
  );
}
```

**Что делает:**
- Отображает найденные рецепты
- Если рецептов нет - показывает текст подсказки

---

### 3️⃣ **Chat** - Чат с AI кулинаром

```jsx
function Chat() {
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Добавляем сообщение пользователя
    const newMessages = [...messages, { role: 'user', text: input }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      // Отправляем запрос на backend
      const response = await fetch('/api/question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
      });

      const data = await response.json();

      // Добавляем ответ от AI
      setMessages([...newMessages, { role: 'ai', text: data.answer }]);
    } catch (error) {
      console.error('Ошибка:', error);
    }

    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h2>🤖 Спросите AI кулинара</h2>
      
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="message ai">Думаю...</div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Задайте вопрос о кулинарии..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
        />
        <button onClick={handleSendMessage}>Отправить</button>
      </div>
    </div>
  );
}
```

**Что делает:**
- Чат интерфейс
- Отправляет вопросы на backend
- Отображает ответы от AI

---

## 🔗 Главный компонент App.js

```jsx
import React from 'react';
import './App.css';
import RecipeForm from './components/RecipeForm';
import RecipeList from './components/RecipeList';
import Chat from './components/Chat';

function App() {
  const [recipes, setRecipes] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleSearch = async (ingredients) => {
    setLoading(true);
    try {
      const response = await fetch('/api/recipes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients })
      });

      const data = await response.json();
      setRecipes(data.recipes);
    } catch (error) {
      console.error('Ошибка:', error);
      setRecipes('Ошибка при получении рецептов');
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🍳 AI Culinary Assistant</h1>
        <p>Умный помощник для генерации рецептов</p>
      </header>

      <main className="main-content">
        <RecipeForm onSearch={handleSearch} />
        {loading && <div className="loader">⏳ Ищу рецепты...</div>}
        <RecipeList recipes={recipes} />
        <Chat />
      </main>

      <footer className="footer">
        <p>© 2024 AI Culinary Assistant. Powered by Google Gemini</p>
      </footer>
    </div>
  );
}

export default App;
```

---

## 📦 package.json - Конфигурация проекта

```json
{
  "name": "ai-culinary-assistant-frontend",
  "version": "1.0.0",
  "description": "Frontend для AI Culinary Assistant",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

---

## 🚀 Как запустить React приложение?

### Шаг 1: Установить зависимости
```bash
cd frontend
npm install
```

### Шаг 2: Запустить dev сервер
```bash
npm start
```

**Результат:**
```
Compiled successfully!

You can now view ai-culinary-assistant in the browser.

  Local:            http://localhost:3000
```

---

## 💡 Ключевые концепции React

| Концепция | Что это |
|-----------|--------|
| **Component** | Переиспользуемый кусок UI |
| **JSX** | HTML-подобный синтаксис в JavaScript |
| **Props** | Параметры, которые передаются компоненту |
| **State** | Данные, которые могут меняться |
| **Render** | Отображение компонента в браузере |

---

## ✅ Запомните

1. **React** = библиотека для создания интерфейсов
2. **Компонент** = функция, которая возвращает JSX
3. **JSX** = HTML внутри JavaScript
4. **Props** = параметры компонента (входные данные)
5. **State** = внутренние данные компонента

Дальше: **HTTP запросы и как frontend общается с backend!** 🚀
