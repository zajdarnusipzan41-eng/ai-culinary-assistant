import React from 'react';

function RecipeList({ recipes }) {
  if (!recipes || !Array.isArray(recipes) || recipes.length === 0) {
    return (
      <div className="recipes-container">
        <h2>📖 Рецепты</h2>
        <p className="no-recipes">
          Введите ингредиенты выше и нажмите "Найти рецепты" 👆
        </p>
      </div>
    );
  }

  return (
    <div className="recipes-container">
      <h2>📖 Найденные рецепты ({recipes.length})</h2>
      <div className="recipes-grid">
        {recipes.map((recipe, index) => (
          <div key={index} className="recipe-card">
            <div className="recipe-header">
              <h3>{recipe.title}</h3>
              <span className={`badge difficulty-${recipe.difficulty?.toLowerCase()}`}>
                {recipe.difficulty}
              </span>
            </div>

            <p className="cooking-time">⏱ Время: {recipe.cooking_time}</p>

            {recipe.ingredients_used && recipe.ingredients_used.length > 0 && (
              <div className="recipe-ingredients">
                <h4>Ингредиенты:</h4>
                <ul>
                  {recipe.ingredients_used.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {recipe.steps && recipe.steps.length > 0 && (
              <div className="recipe-steps">
                <h4>Инструкция по приготовлению:</h4>
                <ol>
                  {recipe.steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecipeList;
