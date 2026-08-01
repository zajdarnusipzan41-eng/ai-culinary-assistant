import React from 'react';

function RecipeList({ recipes }) {
  if (!recipes) {
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
      <h2>📖 Найденные рецепты</h2>
      <div className="recipe-content">
        {recipes}
      </div>
    </div>
  );
}

export default RecipeList;
