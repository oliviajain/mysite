from flask import Flask, render_template, jsonify
from recipes import recipes 

app = Flask(__name__)

def get_all_ingredients(): 
    all_ingredients = set()
    for recipe_name, recipe in recipes.items(): 
        all_ingredients.update(recipe['ingredients'])
    return all_ingredients

@app.route('/')
def index(): 
    ingredients = get_all_ingredients()
    return render_template('index.html', recipes=list(recipes.keys()), ingredients=list(ingredients))

@app.route('/recipes/<recipe_name>')
def recipe(recipe_name):
    return render_template("recipe.html", recipe=recipes.get(recipe_name))

if __name__ == '__main__':
    app.run(debug=True)
