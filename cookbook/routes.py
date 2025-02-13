from flask import Blueprint, Flask, render_template, jsonify, request, redirect
from .recipes import recipes
import os

cookbook_bp = Blueprint('cookbook', __name__, url_prefix='/cookbook')

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
    return {x['name']: x['missing'] for x in infos[:5]}


def get_recipe_photos():
    return [{'src': value.get('image'),
            'caption': key,
             'link': f'recipe/{key}',
             }
            for key, value in recipes.items()]


@cookbook_bp.route("/handle_form_submit", methods=['POST'])
def handle_form_submit():
    selected_ingredients = request.get_json().get('selectedOptions')
    tops = get_top_recipes(selected_ingredients)
    return tops


@cookbook_bp.route('/', methods=['GET', 'POST'])
def index():
    ingredients = get_all_ingredients()
    photos = get_recipe_photos()
    return render_template('cookbook/index.html', ingredients=list(ingredients), photos=list(photos))


@cookbook_bp.route('/about')
def about():
    return render_template("cookbook/about.html", ingredients=list(get_all_ingredients()))


@cookbook_bp.route('/recipes')
def list_recipes():
    photos = get_recipe_photos()
    return render_template("cookbook/recipes.html", photos=list(photos))


@cookbook_bp.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    return render_template("cookbook/recipe.html", recipe=recipes.get(recipe_name))