from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    g,
    Markup,
    flash,
    jsonify,
)
from flask.ext.bcrypt import (
    check_password_hash,
)
from flask.ext.login import (
    current_user,
    LoginManager,
    login_required,
    logout_user,
    login_user,
)

import forms
import models
import requests
import sendgrid
import markdown

COLORS = {
    "Ruby": "#F7464A",
    "Android": "#51B46D",
    "JavaScript": "#C25975",
    "Python": "#F092B0",
    "HTML": "#39ADD1",
    "CSS": "#3079AB",
    "PHP": "#7D669E",
    "Development Tools": "#637A91",
    "Business": "#F9845B",
    "iOS": "#53BBB4",
    "Design": "#E0AB18",
    "Java": "#2C9676",
    "WordPress": "#838CC7",
    "Digital Literacy": "#C38CD4",
}
NUMBER_OF_COURSES = 12
TREEHOUSE_USER = "charliethomas"

key = open("key.txt")

app = Flask(__name__)
app.secret_key = key.readline().strip("\n")

sendgrid_username = key.readline().strip("\n")
sendgrid_password = key.readline().strip("\n")
print(sendgrid_username, sendgrid_password)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Functions
def remove_space(string):
    return string.replace(" ","-")

def get_points():
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                subject_points = json["points"]  # Get points
                return subject_points
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def get_number_of_subjects():
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                subject_points = json["points"]  # Get points
                return len(subject_points)
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def get_courses(number_of_courses):
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                badges = json["badges"]  # Get points
                badges = badges[-number_of_courses:]
                badges.reverse()
                return badges
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def order_points(points):
    return sorted(points.items(), key=lambda x: x[1])[::-1]


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each response"""
    g.db.close()
    return response

@app.route("/login/", methods=("GET", "POST"))
@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.User.DoesNotExist:
            flash("Your email or password does not exist.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in.", "success")
                return redirect(url_for("index"))
            else:
                flash("Your email or password does not exist.", "error")
    return render_template("login.html", form=form)

@app.route("/logout/")
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Come back soon.")
    return redirect(url_for("index"))

@app.route("/new_post/", methods=("POST", "GET"))
@app.route("/new_post", methods=("POST", "GET"))
@login_required
def new_post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(
            user_id=g.user.get_id(),
            title=form.title.data.strip(),
            description=form.description.strip()
        )
        flash("Posted! Thanks!", "success")
        return redirect(url_for("index"))
    return render_template("add_post.html", form=form)

@app.route("/new_project/", methods=("POST", "GET"))
@app.route("/new_project", methods=("POST", "GET"))
@login_required
def new_project():
    form = forms.ProjectForm()
    if form.validate_on_submit():
        models.Project.create(
            user_id=g.user.get_id(),
            title=form.title.data.strip(),
            link=form.link.data.strip(),
            description=form.description.data.strip()
        )
        flash("Posted! Thanks!", "success")
        return redirect(url_for("index"))
    return render_template("add_project.html", form=form)


@app.route("/")
def index():
    posts = models.Post.get_posts()
    return render_template("show.html", posts=posts)


@app.route("/about/")
@app.route("/about")
def about():
    """Route for about page"""
    return render_template("about.html")


@app.route("/portfolio/")
@app.route("/portfolio")
def portfolio():
    """Route for portfolio page"""
    projects = models.Project.get_projects()
    for project in projects:
        unicode_body = project["description"]
        html_body = markdown.markdown(unicode_body)
        safe_html_body = Markup(html_body)
        project["description"] = safe_html_body
    context = {
        "projects": projects,
    }
    return render_template("portfolio.html", **context)


@app.route("/points/")
@app.route("/points")
def points():
    """points = order_points(get_points())
    courses = get_courses(NUMBER_OF_COURSES)
    context = {
        "points": points,
        "courses": courses,
        "colors": COLORS,
        "username": TREEHOUSE_USER,
    }"""
    return render_template("points.html", username=TREEHOUSE_USER)


@app.route("/contact/", methods=["POST", "GET"])
@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = forms.ContactForm()
    if form.validate_on_submit():
        sendgrid_object = sendgrid.SendGridClient(
            sendgrid_username, sendgrid_password)
        message = sendgrid.Mail()
        sender = form.email.data
        subject = form.name.data
        body = form.body.data
        message.add_to("charlie.thomas@attwoodthomas.net")
        message.set_from(sender)
        message.set_subject(subject)
        message.set_html(body)
        sendgrid_object.send(message)
        flash("Email sent.")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html", form=form)


@app.route("/post/<id>/")
@app.route("/post/<id>")
def post(id):
    """Page for each post. It shows the title and body of a given post.

    Parameters:
    id - init - id for post to view

    Template: post.html
    Redirect: None
    """
    post = models.Post.get(models.Post.id == id)
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


@app.route("/update/<id>/", methods=["POST", "GET"])
@app.route("/update/<id>", methods=["POST", "GET"])
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
    form = forms.PostForm()
    post = models.Post.get(models.Post.id == id)
    print(post.title)
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.body = form.description.data
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


@app.route("/delete/<id>/")
@app.route("/delete/<id>")
@login_required
def delete(id):
    try:
        project = models.Post.get(models.Post.id == id)
        project.delete_instance()
        result = "Success."
    except:
        result = "Error."
    flash(result)
    return redirect(url_for("index"))


@app.route("/add/", methods=["POST", "GET"])
@app.route("/add", methods=["POST", "GET"])
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
    form = forms.PostForm()
    if form.validate_on_submit():
        try:
            models.Post.create_post(
                title=form.title.data,
                body=form.description.data,
                user_id=current_user.get_id()
            )
            result = "Success"
        except:
            result = "Error."
        flash(result)
        return redirect(url_for("index"))
    else:
        return render_template("add_post.html", form=form)


@app.route("/update_project/<id>/", methods=["POST", "GET"])
@app.route("/update_project/<id>", methods=["POST", "GET"])
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
    form = forms.ProjectForm()
    project = models.Project.get(models.Project.id == id)
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


@app.route("/delete_project/<id>/")
@app.route("/delete_project/<id>")
@login_required
def delete_project(id):
    """Route to delete project from id.

    Parameters:
    id - int - id for project to delete

    Template: None
    Redirect: portfolio
    """
    try:
        project = models.Project.get(models.Project.id == id)
        project.delete_instance()
        result = "Success."
    except:
        result = "Error."
    flash(result)
    return redirect(url_for("portfolio"))


@app.route("/add_project/", methods=["POST", "GET"])
@app.route("/add_project", methods=["POST", "GET"])
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
    form = forms.ProjectForm()
    if form.validate_on_submit():
        result = models.Project.create_project(
            title=form.title.data,
            link=form.link.data,
            body=form.description.data,
            user_id=current_user.get_id()
        )
        flash(result)
        return redirect(url_for("portfolio"))
    else:
        return render_template("add_project.html", form=form)

@app.route("/post_json/", methods=["POST", "GET"])
@app.route("/post_json", methods=["POST", "GET"])
def post_json():
    posts = models.Post.get_posts()[::-1]
    return jsonify(results=posts)

@app.route("/science")
def science():
    return render_template("science.html")

if __name__ == "__main__":
    app.jinja_env.filters['remove_space'] = remove_space
    app.run(debug=True)
