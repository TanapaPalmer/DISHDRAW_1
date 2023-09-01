from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models.user import User
from flask import flash

# ---------------------------------------------------
# "Recipe" CLASS

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.ingredients = data['ingredients']
        self.directions = data['directions']
        self.notes = data['notes']
        self.servings = data['servings']
        self.prep_time = data['prep_time']
        self.cooking_time = data['cooking_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']        
        self.user_id = data['user_id']
        self.poster = None
        
# ---------------------------------------------------
# VALIDATIONS

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 5:
            flash("Name must be at least 5 characters long","recipes")
            is_valid = False
        if len(data['ingredients']) < 20:
            flash("Ingredients must be at least 20 characters long","recipes")
            is_valid = False
        if len(data['directions']) < 20:
            flash("Directions must be at least 20 characters long","recipes")
            is_valid = False
        if len(data['servings']) < 1:
            flash("Servings can not be blank","recipes")
            is_valid = False
        if len(data['prep_time']) < 1:
            flash("Prepping Time can not be blank","recipes")
            is_valid = False
        if len(data['cooking_time']) < 1:
            flash("Cooking Time can not be blank","recipes")
            is_valid = False
            
        return is_valid
    
# ---------------------------------------------------
# GET ALL RECIPES

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL('dish_draw').query_db(query)
        recipes = []
        for row in results:
            one_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_recipe.poster = user.User(user_data)
            recipes.append(one_recipe)
        return recipes 

# ---------------------------------------------------
# GET RECIPE BY ID

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query,data)
        if result:
            name = cls(result[0])
            return name
        else:
            return False

# ---------------------------------------------------
# SAVE A RECIPE

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name,ingredients,directions,notes,servings,prep_time,cooking_time,created_at,updated_at) VALUES (%(name)s,%(ingredients)s,%(directions)s,%(notes)s,%(servings)s,%(prep_time)s,%(cooking_time)s,%(created_at)s,%(updated_at)s;"
        return connectToMySQL('dish_draw').query_db(query,data)

# ---------------------------------------------------
# UPDATE A RECIPE

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, ingredients = %(ingredients)s, directions = %(directions)s, notes = %(notes)s, servings = %(servings)s, prep_time = %(prep_time)s, cooking_time = %(cooking_time)s, created_at = %(created_at)s, updated_at = %(updated_at)s WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query,data)
        return result

# ---------------------------------------------------
# DELETE A RECIPE

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query,data)
        return result

