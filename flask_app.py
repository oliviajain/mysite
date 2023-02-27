from flask import Flask, render_template, jsonify, request, redirect
from recipes import recipes 

app = Flask(__name__)

def get_all_ingredients(): 
    all_ingredients = set()
    for _, recipe in recipes.items(): 
        all_ingredients.update(recipe['ingredients'])    
    return sorted(all_ingredients)

def get_top_recipes(selected_ingredients): 
    ingredients = set(selected_ingredients)
    infos = []
    for recipe_name, recipe in recipes.items():
        recipe_ingredients = set(recipe['ingredients'])
        missing = recipe_ingredients.difference(ingredients)
        infos.append({'name': recipe_name, 'missing': list(missing)})
    infos.sort(key=lambda x: len(x['missing']))
    return infos[:5]
    

@app.route("/handle_form_submit", methods=['POST'])
def handle_form_submit():
    selected_ingredients = request.get_json().get('selectedOptions')
    tops = get_top_recipes(selected_ingredients)
    return tops

@app.route('/', methods=['GET', 'POST'])
def index(): 
    ingredients = get_all_ingredients()
    return render_template('index.html', recipes=sorted(recipes.keys()), ingredients=list(ingredients))

@app.route('/about')
def about():
    return render_template("about.html", ingredients=list(get_all_ingredients()))

@app.route('/recipes')
def list_recipes():
    return render_template("recipes.html", recipes=sorted(recipes.keys()))

@app.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    return render_template("recipe.html", recipe=recipes.get(recipe_name))

if __name__ == '__main__':
    app.run(debug=True)
