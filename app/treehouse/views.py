from flask import Blueprint, render_template

from app.treehouse.constants import TREEHOUSE_USER

treehouse_blueprint = Blueprint("treehouse_blueprint", __name__)

@treehouse_blueprint.route("/points/")
@treehouse_blueprint.route("/points")
def points():
    return render_template("points.html", username=TREEHOUSE_USER)