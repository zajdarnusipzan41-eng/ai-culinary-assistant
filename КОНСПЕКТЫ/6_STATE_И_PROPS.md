# 🔄 КОНСПЕКТ 6: State и Props в React

## 📚 Что такое State и Props?

**State** = внутренние данные компонента (могут меняться)
**Props** = параметры, которые передаются компоненту (не меняются внутри)

### Аналогия из жизни:

```
Компонент = функция/инструмент

Props = входные параметры функции (аргументы)
function getRecipe(ingredients) {  // ingredients = Props
  ...
}

State = переменные внутри функции (локальные данные)
function App() {
  let recipes = [];  // State
  ...
}
```

---

## 📥 Props - входные параметры

### Как передавать Props?

```jsx
// 1. Родительский компонент (App.js)
function App() {
  return (
    <RecipeForm title="Введите ингредиенты" maxItems={10} />
  );
}

// 2. Дочерний компонент (RecipeForm.js) получает Props
function RecipeForm(props) {
  return (
    <div>
      <h2>{props.title}</h2>
      <p>Максимум: {props.maxItems} ингредиентов</p>
    </div>
  );
}
```

**Результат:**
```
Введите ингредиенты
Максимум: 10 ингредиентов
```

---

### Деструктуризация Props (лучше)

```jsx
// Старый способ
function RecipeForm(props) {
  return <h2>{props.title}</h2>;
}

// Новый способ ✅
function RecipeForm({ title, maxItems }) {
  return (
    <div>
      <h2>{title}</h2>
      <p>Максимум: {maxItems}</p>
    </div>
  );
}
```

---

### Props в нашем проекте

```jsx
// App.js (родитель)
function App() {
  const [recipes, setRecipes] = React.useState(null);

  return (
    <RecipeForm onSearch={handleSearch} />
    <RecipeList recipes={recipes} />
  );
}

// RecipeForm.js (дочерний компонент)
function RecipeForm({ onSearch }) {
  return (
    <button onClick={() => onSearch(['яйцо'])}>
      Поиск
    </button>
  );
}

// RecipeList.js (дочерний компонент)
function RecipeList({ recipes }) {
  return (
    <div>
      {recipes ? <p>{recipes}</p> : <p>Нет рецептов</p>}
    </div>
  );
}
```

---

## 🔄 State - внутренние данные

### Как создать State?

```jsx
import React from 'react';

function Counter() {
  // React.useState(начальное значение)
  // Возвращает: [текущее значение, функция для изменения]
  const [count, setCount] = React.useState(0);

  return (
    <div>
      <p>Счётчик: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        +1
      </button>
    </div>
  );
}
```

**Как это работает:**
1. `count = 0` (начальное значение)
2. `setCount` = функция для изменения count
3. `onClick={() => setCount(count + 1)}` = нажата кнопка → увеличили count
4. React видит, что state изменился → перерисовал компонент

---

### Несколько State переменных

```jsx
function RecipeForm() {
  const [ingredients, setIngredients] = React.useState([]);
  const [input, setInput] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const handleAdd = () => {
    if (input.trim()) {
      setIngredients([...ingredients, input]);  // Добавили ингредиент
      setInput('');  // Очистили инпут
    }
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Введите ингредиент"
      />
      <button onClick={handleAdd}>Добавить</button>
      
      {loading && <p>⏳ Загружаю...</p>}
      
      <ul>
        {ingredients.map((ing, i) => (
          <li key={i}>{ing}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 🔄 Жизненный цикл State

```
1. Компонент создан
   const [count, setCount] = useState(0)
   count = 0
                    ↓
2. React рендерит компонент
   <p>Счётчик: 0</p>
                    ↓
3. Пользователь нажимает кнопку
   onClick={() => setCount(count + 1)}
                    ↓
4. State изменяется
   count = 1
                    ↓
5. React ПЕРЕЛИВАЕТ компонент (перерисовал)
   <p>Счётчик: 1</p>
                    ↓
6. На экране: новое значение 1
```

---

## 📊 Props vs State

| Свойство | Props | State |
|----------|-------|-------|
| **Откуда** | От родителя | Внутри компонента |
| **Изменяется** | Нет (только родитель может) | Да (через setState) |
| **Используется для** | Передача данных | Локальные данные |
| **Пример** | `<RecipeForm title="..." />` | `const [count, setCount] = useState(0)` |

---

## 🎯 Полный пример в нашем приложении

```jsx
// App.js (родитель - главный компонент)
import React from 'react';
import RecipeForm from './components/RecipeForm';
import RecipeList from './components/RecipeList';
import Chat from './components/Chat';

function App() {
  // State: то, что может меняться
  const [recipes, setRecipes] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  // Функция для поиска рецептов
  const handleSearch = async (ingredients) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/recipes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients })
      });

      const data = await response.json();

      if (data.success) {
        setRecipes(data.recipes);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Ошибка при получении рецептов');
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <h1>🍳 AI Culinary Assistant</h1>
      
      {/* Props: передаём onSearch в дочерний компонент */}
      <RecipeForm onSearch={handleSearch} />

      {/* Props: передаём recipes и loading */}
      {loading && <p>⏳ Загружаю рецепты...</p>}
      {error && <p style={{color: 'red'}}>Ошибка: {error}</p>}
      
      <RecipeList recipes={recipes} />
      <Chat />
    </div>
  );
}

export default App;
```

```jsx
// RecipeForm.js (дочерний компонент)
import React from 'react';

function RecipeForm({ onSearch }) {
  // State: локальные данные компонента
  const [ingredients, setIngredients] = React.useState([]);
  const [input, setInput] = React.useState('');

  const handleAddIngredient = () => {
    if (input.trim()) {
      // Добавляем ингредиент в список
      setIngredients([...ingredients, input]);
      setInput('');  // Очищаем инпут
    }
  };

  const handleSearch = () => {
    if (ingredients.length > 0) {
      // Props функция: вызываем onSearch из родителя
      onSearch(ingredients);
    }
  };

  const handleRemoveIngredient = (index) => {
    // Удаляем ингредиент по индексу
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  return (
    <div className="form-container">
      <h2>Введите ингредиенты</h2>

      <div className="input-group">
        <input
          type="text"
          placeholder="Например: яйцо"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') handleAddIngredient();
          }}
        />
        <button onClick={handleAddIngredient}>Добавить</button>
      </div>

      <div className="ingredients-list">
        {ingredients.length === 0 ? (
          <p>Ещё нет ингредиентов</p>
        ) : (
          ingredients.map((ingredient, index) => (
            <div key={index} className="ingredient-tag">
              {ingredient}
              <button
                onClick={() => handleRemoveIngredient(index)}
                className="remove-btn"
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>

      <button
        onClick={handleSearch}
        disabled={ingredients.length === 0}
        className="search-btn"
      >
        🔍 Найти рецепты ({ingredients.length})
      </button>
    </div>
  );
}

export default RecipeForm;
```

```jsx
// RecipeList.js (дочерний компонент)
function RecipeList({ recipes }) {
  if (!recipes) {
    return (
      <div className="recipes-container">
        <p className="no-recipes">Введите ингредиенты для поиска рецептов</p>
      </div>
    );
  }

  return (
    <div className="recipes-container">
      <h2>Найденные рецепты</h2>
      <div className="recipe-content">
        {recipes}
      </div>
    </div>
  );
}

export default RecipeList;
```

```jsx
// Chat.js (дочерний компонент)
import React from 'react';

function Chat() {
  // State: история сообщений и текущий ввод
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Добавляем сообщение пользователя
    const userMessage = { role: 'user', text: input };
    setMessages([...messages, userMessage]);
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
      const aiMessage = { role: 'ai', text: data.answer };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Ошибка:', error);
      const errorMessage = { role: 'ai', text: 'Произошла ошибка' };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h2>🤖 AI Кулинар</h2>

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {loading && <div className="message ai"><p>Думаю...</p></div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Задайте вопрос о кулинарии..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') handleSendMessage();
          }}
          disabled={loading}
        />
        <button onClick={handleSendMessage} disabled={loading}>
          {loading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
}

export default Chat;
```

---

## 🔗 Поток данных в нашем приложении

```
                    App.js
                 (родитель)
                     |
          [recipes, setRecipes]  ← State
                     |
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    RecipeForm   RecipeList    Chat
    (дочерний)   (дочерний)   (дочерний)
        |            |            |
      Props:       Props:       State:
      onSearch     recipes      messages
                                input
```

**Как работает:**
1. Пользователь вводит в RecipeForm
2. RecipeForm вызывает `onSearch(ingredients)` (Props функция)
3. App получает ингредиенты и делает запрос на backend
4. Backend возвращает рецепты
5. App обновляет `setRecipes(data.recipes)` (State)
6. React переливает RecipeList с новыми Props
7. RecipeList показывает рецепты пользователю

---

## ✅ Запомните

1. **Props** = параметры из родителя (не меняются внутри)
2. **State** = внутренние данные компонента (меняются)
3. **useState()** = хук для создания state переменной
4. **setXXX()** = функция для изменения state
5. **React рендерит** = когда state или props меняются
6. **Один props** из родителя = один компонент может это получить

---

## 🎯 Ключевые функции

```javascript
// Создать state
const [value, setValue] = React.useState(initialValue);

// Прочитать state
console.log(value);

// Изменить state
setValue(newValue);

// State массив
const [arr, setArr] = React.useState([]);
setArr([...arr, newItem]);  // Добавить элемент
setArr(arr.filter((_, i) => i !== index));  // Удалить

// State объект
const [obj, setObj] = React.useState({});
setObj({...obj, key: value});  // Обновить
```

---

## 🚀 Готовый к использованию паттерн

```jsx
function MyComponent({ prop1, prop2, onAction }) {
  // State
  const [data, setData] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  // Обработчик
  const handleAction = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: prop1 })
      });

      const result = await response.json();
      setData(result);
      onAction(result);  // Props функция
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div>
      {loading && <p>⏳</p>}
      {error && <p>{error}</p>}
      {data && <p>{data}</p>}
      <button onClick={handleAction}>Action</button>
    </div>
  );
}
```

---

## ✨ Итог

**State** и **Props** - это суть React!

- **Props** = как функция принимает аргументы
- **State** = как функция хранит переменные
- **React** = автоматически переливает когда они меняются

Это всё, что нужно знать для начала! 🚀
