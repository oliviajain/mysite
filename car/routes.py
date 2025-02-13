from flask import Blueprint, send_from_directory, render_template

car_bp = Blueprint('car', __name__, url_prefix='/car')

@car_bp.route('/')
def index():
    return render_template('car/home.html')
    # return send_from_directory('static/car', 'car.png')