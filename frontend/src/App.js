import React from 'react';
import './App.css';
import RecipeForm from './components/RecipeForm';
import RecipeList from './components/RecipeList';
import Chat from './components/Chat';

function App() {
  const [recipes, setRecipes] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

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
        setError(data.error || 'Ошибка при получении рецептов');
      }
    } catch (err) {
      console.error('Ошибка:', err);
      setError('Ошибка при подключении к серверу');
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>🍳 AI Culinary Assistant</h1>
          <p>Умный помощник для генерации рецептов на основе AI</p>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          <RecipeForm onSearch={handleSearch} />

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>⏳ Ищу вкусные рецепты...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <p>❌ {error}</p>
            </div>
          )}

          <RecipeList recipes={recipes} />
          <Chat />
        </div>
      </main>

      <footer className="footer">
        <p>© 2024 AI Culinary Assistant</p>
        <p>Powered by Google Gemini & React</p>
      </footer>
    </div>
  );
}

export default App;
