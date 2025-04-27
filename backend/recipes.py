from flask_restx import Namespace, Resource, fields
from flask import request,abort
from backend.models import Recipe  # make sure this is where Recipe is defined
from backend.exts import db  # assuming db is initialized here
from flask_jwt_extended import jwt_required



# Create a Namespace
recipe_ns = Namespace('recipe', description="A namespace for Recipes")

# Swagger model for Recipe
recipe_model = recipe_ns.model(
    "Recipe",
    {
        "id": fields.Integer(readOnly=True),
        "title": fields.String(required=True, description="Recipe title"),
        "description": fields.String(description="Recipe description")
    }
)

# -------------------- Routes --------------------

@recipe_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World"}

@recipe_ns.route('/recipes')
class RecipesResource(Resource):
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        recipes = Recipe.query.all()
        return recipes

    @recipe_ns.expect(recipe_model)
    @recipe_ns.marshal_with(recipe_model, code=201)
    def post(self):
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get('title'),
            description=data.get('description')
        )
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe, 201

@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @recipe_ns.marshal_with(recipe_model)
    def get(self, id):
        recipe = db.session.get(Recipe, id)
        if not recipe:
            abort(404, description="Recipe not found")
        return recipe

    @recipe_ns.expect(recipe_model)
    @recipe_ns.marshal_with(recipe_model)
    def put(self, id):
        data = request.get_json()
        recipe = db.session.get(Recipe, id)
        if not recipe:
            abort(404, description="Recipe not found")

        recipe.title = data.get('title')
        recipe.description = data.get('description')
        db.session.commit()
        return recipe

    def delete(self, id):
        recipe = db.session.get(Recipe, id)
        if not recipe:
           abort(404, description="Recipe not found")

        db.session.delete(recipe)
        db.session.commit()
        return {"message": "Recipe deleted successfully"}, 204
