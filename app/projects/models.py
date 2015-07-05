from app.models import BaseModel, User

from peewee import CharField, TextField, ForeignKeyField, DateTimeField

import datetime

class Project(BaseModel):
    """A model for a project containing a title and a description"""
    user_id = ForeignKeyField(rel_model=User)
    title = CharField()
    link = CharField()
    description = TextField()

    @classmethod
    def create_project(cls, title, description, user_id, link):
        cls.create(
            title=title,
            description=description,
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