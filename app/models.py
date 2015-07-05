from peewee import (
    Model,
    MySQLDatabase,
    SqliteDatabase,
    CharField,
    IntegrityError,
    ForeignKeyField,
    TextField,
    DateTimeField,
)
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
import datetime

DATABASE = SqliteDatabase("MY_SITE_DB.db")


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






def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Project])
    DATABASE.close()
