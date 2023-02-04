from flask import Flask, render_template, jsonify
from recipes import recipes 

app = Flask(__name__)

@app.route('/')
def index(): 
    print(recipes)
    return render_template('index.html', recipes=list(recipes.keys()))

@app.route('/chocolate_cake')
def chocolate_cake(): 
    return render_template("recipe.html", recipe=recipes.get('Chocolate Cake'))

if __name__ == '__main__':
    app.run(debug=True)