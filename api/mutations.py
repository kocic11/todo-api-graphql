from datetime import datetime

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Todo


# pylint: disable=C, unnecessary-pass, wrong-import-order, no-member

@convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, description, due_date):
    print(f"Obj: {obj}, Info: {info}")
    try:
        due_date = datetime.strptime(due_date, '%d-%m-%Y').date()
        todo = Todo(
            description=description, due_date=due_date
        )
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except ValueError:  # date time errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format dd-mm-yyyy"]
        }

    return payload


@convert_kwargs_to_snake_case
def resolve_mark_done(obj, info, todo_id):
    print(f"Obj: {obj}, Info: {info}")
    try:
        todo = Todo.query.get(todo_id)
        todo.completed = True
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors":  [f"Todo matching id {todo_id} was not found"]
        }

    return payload


@convert_kwargs_to_snake_case
def resolve_delete_todo(obj, info, todo_id):
    print(f"Obj: {obj}", "Info: {info}")
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }

    return payload


@convert_kwargs_to_snake_case
def resolve_update_due_date(obj, info, todo_id, new_date):
    print(f"Obj: {obj}", "Info: {info}")
    try:
        todo = Todo.query.get(todo_id)
        if todo:
            todo.due_date = datetime.strptime(new_date, '%d-%m-%Y').date()
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }

    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format dd-mm-yyyy"]
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }
    return payload
