from flask import Blueprint

wedding_bp = Blueprint('wedding', __name__)

from wedding import routes
