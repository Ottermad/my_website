from flask import Blueprint, g, redirect, url_for, render_template, flash, Markup

from flask.ext.login import login_required

from app.posts.forms import PostForm

from app.posts.models import Post

import markdown

posts_blueprint = Blueprint("posts_blueprint", __name__)

@posts_blueprint.route("/")
def index():
    posts = Post.get_posts()
    return render_template("show.html", posts=posts)


@posts_blueprint.route("/post/<id>/")
@posts_blueprint.route("/post/<id>")
def post(id):
    """Page for each post. It shows the title and body of a given post.

    Parameters:
    id - init - id for post to view

    Template: post.html
    Redirect: None
    """
    post = Post.get(Post.id == id)
    title = post.title
    posted_at = post.posted_at
    body = post.body
    unicode_body = body
    html_body = markdown.markdown(unicode_body)
    safe_html_body = Markup(html_body)
    context = {
        "title": title,
        "posted_at": posted_at,
        "body": safe_html_body,
        "url": url_for("post", id=id)
    }
    return render_template("post.html", **context)

@posts_blueprint.route("/update/<id>/", methods=["POST", "GET"])
@posts_blueprint.route("/update/<id>", methods=["POST", "GET"])
@login_required
def update(id):
    """Route to update post the function has two operations based on the
    request method.

    Parameters:
    id - init - id for post to update

    GET method:
    If the request method is GET it loads the form to update the post.

    Template: edit.html
    Redirect: None

    POST method:
    If the request method is POST then it updates the post based on the id
    with the title and body.

    Template: None
    Redirect: show
    """
    form = PostForm()
    post = Post.get(Post.id == id)
    print(post.title)
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.body = form.body.data
            post.save()
            result = "Success"
        except:
            result = "Error"
        flash(result)
        return redirect(url_for("index"))
    else:
        ids = [form.title.id, form.description.id]
        body = post.body.replace("\n", "|").replace("\r", "")
        print(body)
        values = [post.title, body]
        context = {
            "form": form,
            "ids": ids,
            "values": values
        }
        print(context)
        return render_template("update_post.html", **context)


@posts_blueprint.route("/delete/<id>/")
@posts_blueprint.route("/delete/<id>")
@login_required
def delete(id):
    try:
        project = Post.get(Post.id == id)
        project.delete_instance()
        result = "Success."
    except:
        result = "Error."
    flash(result)
    return redirect(url_for("index"))


@posts_blueprint.route("/add/", methods=["POST", "GET"])
@posts_blueprint.route("/add", methods=["POST", "GET"])
@login_required
def add():
    """Route to add post. The function has two operations based on the request
    method

    Parameters:
    None

    GET method:
    If the request method is GET it loads the form to add a post.

    Template: add.html
    Redirect: None

    POST method:
    If the request method is POST then it adds the post with the title and
    body.

    Template: None
    Redirect: show
    """
    form = PostForm()
    if form.validate_on_submit():
        try:
            Post.create_post(
                title=form.title.data,
                body=form.body.data,
                user_id=g.user.get_id()
            )
            result = "Success"
        except:
            result = "Error."
        flash(result)
        return redirect(url_for("index"))
    else:
        return render_template("add_post.html", form=form)
