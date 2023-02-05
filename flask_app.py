from flask import Flask, render_template, jsonify
from recipes import recipes 

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html', recipes=list(recipes.keys()))

@app.route('/recipes/<recipe_name>')
def recipe(recipe_name):
    return render_template("recipe.html", recipe=recipes.get(recipe_name))

if __name__ == '__main__':
    app.run(debug=True)
