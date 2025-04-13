const _URL = "http://127.0.0.1:5000/recipes"; // adjust if needed

document.getElementById("recipeForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  await fetch(_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description })
  });

  document.getElementById("recipeForm").reset();
  loadRecipes();
});

async function loadRecipes() {
  const res = await fetch(_URL);
  const recipes = await res.json();

  const container = document.getElementById("recipes");
  container.innerHTML = "";
  recipes.forEach(r => {
    const div = document.createElement("div");
    div.className = "recipe";
    div.innerHTML = `
      <h3>${r.title}</h3>
      <p>${r.description}</p>
      <button onclick="deleteRecipe(${r.id})">Delete</button>
    `;
    container.appendChild(div);
  });
}

async function deleteRecipe(id) {
  await fetch(`http://127.0.0.1:5000/recipe/${id}`, {
    method: "DELETE"
  });
  loadRecipes();
}

loadRecipes();
