import logging
from datetime import datetime
from flask import request
from flask_login import login_required, current_user
from app.tasks import tasks_bp
from app.tasks.models import Task, Project, TaskStatus
from app.tasks.services import (
    create_task, update_task, delete_task,
    create_project, update_project, delete_project,
)
from app.shared import success_response, error_response

logger = logging.getLogger(__name__)


@tasks_bp.route("/tasks", methods=["GET"])
@login_required
def list_tasks():
    query = Task.query.filter_by(user_id=current_user.id)
    status = request.args.get("status")
    project_id = request.args.get("project_id")
    if status:
        try:
            query = query.filter_by(status=TaskStatus(status))
        except ValueError:
            return error_response(f"Invalid status: {status}", 400)
    if project_id:
        query = query.filter_by(project_id=project_id)
    tasks = query.order_by(Task.created_at.desc()).all()
    return success_response(data=[t.to_dict() for t in tasks])


@tasks_bp.route("/tasks", methods=["POST"])
@login_required
def create_task_route():
    data = request.get_json()
    if not data or not data.get("title"):
        return error_response("Title is required", 400)

    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except (ValueError, TypeError):
            return error_response("Invalid due_date format", 400)

    task = create_task(
        user_id=current_user.id,
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "todo"),
        priority=data.get("priority", "medium"),
        project_id=data.get("project_id"),
        due_date=due_date,
    )
    return success_response(data=task.to_dict(), status=201)


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
@login_required
def get_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return error_response("Task not found", 404)
    return success_response(data=task.to_dict())


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
@login_required
def update_task_route(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return error_response("Task not found", 404)

    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)

    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(data["due_date"])
        except (ValueError, TypeError):
            return error_response("Invalid due_date format", 400)

    updated = update_task(
        task,
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status"),
        priority=data.get("priority"),
        project_id=data.get("project_id"),
        due_date=due_date,
    )
    return success_response(data=updated.to_dict())


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
@login_required
def delete_task_route(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return error_response("Task not found", 404)
    delete_task(task)
    return success_response(message="Task deleted")


@tasks_bp.route("/projects", methods=["GET"])
@login_required
def list_projects():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_at.desc()).all()
    return success_response(data=[p.to_dict() for p in projects])


@tasks_bp.route("/projects", methods=["POST"])
@login_required
def create_project_route():
    data = request.get_json()
    if not data or not data.get("name"):
        return error_response("Name is required", 400)

    project = create_project(
        user_id=current_user.id,
        name=data["name"],
        description=data.get("description"),
    )
    return success_response(data=project.to_dict(), status=201)


@tasks_bp.route("/projects/<project_id>", methods=["GET"])
@login_required
def get_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        return error_response("Project not found", 404)
    data = project.to_dict()
    data["tasks"] = [t.to_dict() for t in project.tasks]
    return success_response(data=data)


@tasks_bp.route("/projects/<project_id>", methods=["PUT"])
@login_required
def update_project_route(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        return error_response("Project not found", 404)

    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)

    updated = update_project(project, name=data.get("name"), description=data.get("description"))
    return success_response(data=updated.to_dict())


@tasks_bp.route("/projects/<project_id>", methods=["DELETE"])
@login_required
def delete_project_route(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    if not project:
        return error_response("Project not found", 404)
    delete_project(project)
    return success_response(message="Project deleted")
