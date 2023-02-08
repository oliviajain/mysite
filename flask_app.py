from flask import Flask, render_template, jsonify, request, redirect
from recipes import recipes 

app = Flask(__name__)

def get_all_ingredients(): 
    all_ingredients = set()
    for _, recipe in recipes.items(): 
        all_ingredients.update(recipe['ingredients'])
    return all_ingredients

def get_top_recipes(selected_ingredients): 
    ingredients = set(selected_ingredients)
    info = {}
    counts = []
    for recipe_name, recipe in recipes.items():
        recipe_ingredients = set(recipe['ingredients'])
        overlap = recipe_ingredients.intersection(ingredients)
        missing = recipe_ingredients.difference(ingredients)
        info[recipe_name] = {'missing': missing}
        counts.append((len(overlap), recipe_name))
    counts.sort(key=lambda x: x[0], reverse=True)
    tops = counts[:3]
    return {top_recipe[1]: list(info.get(top_recipe[1]).get('missing')) for top_recipe in tops}
       
@app.route("/handle_form_submit", methods=['POST'])
def handle_form_submit():
    selected_ingredients = request.get_json().get('selectedOptions')
    tops = get_top_recipes(selected_ingredients)
    return tops

@app.route('/', methods=['GET', 'POST'])
def index(): 
    ingredients = get_all_ingredients()
    return render_template('index.html', recipes=list(recipes.keys()), ingredients=list(ingredients))

@app.route('/recipes/<recipe_name>')
def recipe(recipe_name):
    return render_template("recipe.html", recipe=recipes.get(recipe_name))

if __name__ == '__main__':
    app.run(debug=True)
