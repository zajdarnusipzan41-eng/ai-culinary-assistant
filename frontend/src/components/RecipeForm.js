import React from 'react';

function RecipeForm({ onSearch }) {
  const [ingredients, setIngredients] = React.useState([]);
  const [input, setInput] = React.useState('');

  const handleAddIngredient = () => {
    if (input.trim() && !ingredients.includes(input.trim())) {
      setIngredients([...ingredients, input.trim()]);
      setInput('');
    }
  };

  const handleSearch = () => {
    if (ingredients.length > 0) {
      onSearch(ingredients);
    }
  };

  const handleRemoveIngredient = (index) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleAddIngredient();
    }
  };

  return (
    <div className="form-container">
      <h2>🥘 Введите ингредиенты</h2>

      <div className="input-group">
        <input
          type="text"
          placeholder="Например: яйцо, масло, мука"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={handleAddIngredient}>Добавить</button>
      </div>

      {ingredients.length > 0 && (
        <div className="ingredients-list">
          {ingredients.map((ingredient, index) => (
            <span key={index} className="ingredient-tag">
              {ingredient}
              <button
                className="remove-btn"
                onClick={() => handleRemoveIngredient(index)}
                type="button"
              >
                ✕
              </button>
            </span>
          ))}
        </div>
      )}

      <button
        onClick={handleSearch}
        className="search-btn"
        disabled={ingredients.length === 0}
      >
        🔍 Найти рецепты ({ingredients.length})
      </button>
    </div>
  );
}

export default RecipeForm;
