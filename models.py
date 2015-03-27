from peewee import (
    Model,
    MySQLDatabase,
    CharField,
    IntegrityError,
    ForeignKeyField,
    TextField,
    DateTimeField,
)
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
import datetime

DATABASE = MySQLDatabase("MY_SITE_DB", user="root", passwd="OttersR0ck")


class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists.")


class Post(BaseModel):
    """A model for Posts which have a title and a body"""
    user_id = ForeignKeyField(rel_model=User)
    title = CharField()
    body = TextField()
    posted_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def create_post(cls, title, body, user_id):
        cls.create(
            title=title,
            body=body,
            user_id=user_id
        )

    @classmethod
    def get_posts(cls):
        """Method to get all posts from db

        Parameters
        cls

        Returns a list of dictionaries.
        The dictionaries will have an id, title and body.
        """
        posts = []
        print("a")
        for post in Post.select().order_by(Post.posted_at.desc()):
            print()
            post_dict = {
                "id": post.id,
                "title": post.title,
                "posted_at": post.posted_at.strftime("%d-%m-%y"),
                "body": post.body
            }
            posts.append(post_dict)
        print(posts)
        return posts


class Project(BaseModel):
    """A model for a project containing a title and a description"""
    user_id = ForeignKeyField(rel_model=User)
    title = CharField()
    link = CharField()
    description = TextField()

    @classmethod
    def create_project(cls, title, body, user_id, link):
        cls.create(
            title=title,
            description=body,
            link=link,
            user_id=user_id
        )

    @classmethod
    def get_projects(cls):
        """Method to get all projects from db

        Parameters
        None

        Returns a list of dictionaries.
        The dictionaries will ave an id, title, description and link
        """
        projects = []
        for project in Project.select():
            project_dict = {
                "id": project.id,
                "title": project.title,
                "link": project.link,
                "description": project.description
            }
            projects.append(project_dict)
        return projects


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Project])
    DATABASE.close()
