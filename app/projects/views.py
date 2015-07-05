from flask import Blueprint, flash, redirect, url_for, render_template, g, Markup

from flask.ext.login import login_required

from app.projects.forms import ProjectForm

from app.projects.models import Project

import markdown

projects_blueprint = Blueprint("projects_blueprint", __name__)


@projects_blueprint.route("/portfolio/")
@projects_blueprint.route("/portfolio")
def portfolio():
    """Route for portfolio page"""
    projects = Project.get_projects()
    for project in projects:
        unicode_body = project["description"]
        html_body = markdown.markdown(unicode_body)
        safe_html_body = Markup(html_body)
        project["description"] = safe_html_body
    context = {
        "projects": projects,
    }
    return render_template("portfolio.html", **context)
    
    
@projects_blueprint.route("/update_project/<id>/", methods=["POST", "GET"])
@projects_blueprint.route("/update_project/<id>", methods=["POST", "GET"])
@login_required
def update_project(id):
    """Route to update project the function has two operations based on the
    request method.

    Parameters:
    id - init - id for project to update

    GET method:
    If the request method is GET it loads the form to update the project.

    Template: edit.html
    Redirect: None

    project method:
    If the request method is project then it updates the project based on the
    id with the title and body.

    Template: None
    Redirect: portfolio
    """
    form = ProjectForm()
    project = Project.get(Project.id == id)
    if form.validate_on_submit():
        try:
            project.title = form.title.data
            project.description = form.description.data
            project.link = form.link.data
            project.save()
            result = "Success"
        except:
            result = "error"
        flash(result)
        return redirect(url_for("portfolio"))
    else:
        ids = [form.title.id, form.description.id, form.link.id]
        print(repr(project.description))
        values = [
            project.title.strip("\n"),
            project.description.replace("\r\n", "|"),
            project.link.strip("\n")
        ]
        context = {
            "form": form,
            "ids": ids,
            "values": values
        }
        return render_template("update_project.html", **context)


@projects_blueprint.route("/delete_project/<id>/")
@projects_blueprint.route("/delete_project/<id>")
@login_required
def delete_project(id):
    """Route to delete project from id.

    Parameters:
    id - int - id for project to delete

    Template: None
    Redirect: portfolio
    """
    try:
        project = Project.get(Project.id == id)
        project.delete_instance()
        result = "Success."
    except:
        result = "Error."
    flash(result)
    return redirect(url_for("portfolio"))


@projects_blueprint.route("/add_project/", methods=["POST", "GET"])
@projects_blueprint.route("/add_project", methods=["POST", "GET"])
@login_required
def add_project():
    """Route to add project. The function has two operations based on the
    request
    method

    Parameters:
    None

    GET method:
    If the request method is GET it loads the form to add a project.

    Template: add.html
    Redirect: None

    POST method:
    If the request method is project then it adds the project with the title
    and body.

    Template: None
    Redirect: portfolio
    """
    form = ProjectForm()
    if form.validate_on_submit():
        result = Project.create_project(
            title=form.title.data,
            link=form.link.data,
            description=form.description.data,
            user_id=g.user.get_id()
        )
        flash(result)
        return redirect(url_for("portfolio"))
    else:
        return render_template("add_project.html", form=form)