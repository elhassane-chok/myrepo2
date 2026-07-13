import logging
from app.extensions import db
from app.tasks.models import Task, Project, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)


def create_task(user_id, title, description=None, status="todo", priority="medium", project_id=None, due_date=None):
    task = Task(
        title=title,
        description=description,
        status=TaskStatus(status),
        priority=TaskPriority(priority),
        project_id=project_id,
        user_id=user_id,
        due_date=due_date,
    )
    db.session.add(task)
    db.session.commit()
    logger.info("Task created: %s by user %s", task.id, user_id)
    return task


def update_task(task, **kwargs):
    if kwargs.get("priority"):
        kwargs["priority"] = TaskPriority(kwargs["priority"])
    if kwargs.get("status"):
        kwargs["status"] = TaskStatus(kwargs["status"])
    for key, value in kwargs.items():
        if value is not None and hasattr(task, key):
            setattr(task, key, value)
    db.session.commit()
    logger.info("Task updated: %s", task.id)
    return task


def delete_task(task):
    db.session.delete(task)
    db.session.commit()
    logger.info("Task deleted: %s", task.id)


def create_project(user_id, name, description=None):
    project = Project(name=name, description=description, user_id=user_id)
    db.session.add(project)
    db.session.commit()
    logger.info("Project created: %s by user %s", project.id, user_id)
    return project


def update_project(project, **kwargs):
    for key, value in kwargs.items():
        if value is not None and hasattr(project, key):
            setattr(project, key, value)
    db.session.commit()
    logger.info("Project updated: %s", project.id)
    return project


def delete_project(project):
    db.session.delete(project)
    db.session.commit()
    logger.info("Project deleted: %s", project.id)
