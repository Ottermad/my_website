from app.models import BaseModel, User

from peewee import CharField, TextField, ForeignKeyField, DateTimeField

import datetime

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
                "posted_at": post.posted_at.strftime("%d/%m/%y"),
                "body": post.body
            }
            posts.append(post_dict)
        print(posts)
        return posts

