import argparse
from datetime import datetime

from db import SessionLocal
from models import Grade, Group, Student, Subject, Teacher


MODEL_MAP = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}

MODEL_FIELDS = {
    "Teacher": ("name",),
    "Group": ("name",),
    "Student": ("name", "group_id"),
    "Subject": ("name", "teacher_id"),
    "Grade": ("grade", "date_received", "student_id", "subject_id"),
}


def get_payload(args, model_name):
    payload = {
        "name": args.name,
        "group_id": args.group_id,
        "teacher_id": args.teacher_id,
        "grade": args.grade,
        "student_id": args.student_id,
        "subject_id": args.subject_id,
    }
    if args.date_received:
        payload["date_received"] = datetime.strptime(args.date_received, "%Y-%m-%d").date()
    return {field: payload[field] for field in MODEL_FIELDS[model_name] if payload.get(field) is not None}


def validate_required_fields(model_name, payload):
    required = set(MODEL_FIELDS[model_name])
    provided = set(payload.keys())
    missed = required - provided
    if missed:
        missed_fields = ", ".join(sorted(missed))
        raise ValueError(f"Missing required fields for {model_name}: {missed_fields}")


def create_entity(session, model_name, payload):
    validate_required_fields(model_name, payload)
    model = MODEL_MAP[model_name]
    entity = model(**payload)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity


def list_entities(session, model_name):
    model = MODEL_MAP[model_name]
    return session.query(model).order_by(model.id).all()


def update_entity(session, model_name, entity_id, payload):
    model = MODEL_MAP[model_name]
    entity = session.query(model).filter(model.id == entity_id).first()
    if not entity:
        return None
    if not payload:
        raise ValueError("No fields provided for update")
    for field, value in payload.items():
        setattr(entity, field, value)
    session.commit()
    session.refresh(entity)
    return entity


def remove_entity(session, model_name, entity_id):
    model = MODEL_MAP[model_name]
    entity = session.query(model).filter(model.id == entity_id).first()
    if not entity:
        return False
    session.delete(entity)
    session.commit()
    return True


def format_entity(entity):
    values = [f"id={entity.id}"]
    if hasattr(entity, "name"):
        values.append(f"name={entity.name}")
    if hasattr(entity, "group_id"):
        values.append(f"group_id={entity.group_id}")
    if hasattr(entity, "teacher_id"):
        values.append(f"teacher_id={entity.teacher_id}")
    if hasattr(entity, "grade"):
        values.append(f"grade={entity.grade}")
    if hasattr(entity, "date_received"):
        values.append(f"date_received={entity.date_received}")
    if hasattr(entity, "student_id"):
        values.append(f"student_id={entity.student_id}")
    if hasattr(entity, "subject_id"):
        values.append(f"subject_id={entity.subject_id}")
    return ", ".join(values)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"])
    parser.add_argument("-m", "--model", required=True, choices=["Teacher", "Group", "Student", "Subject", "Grade"])
    parser.add_argument("--id", type=int)
    parser.add_argument("-n", "--name")
    parser.add_argument("--group-id", type=int)
    parser.add_argument("--teacher-id", type=int)
    parser.add_argument("--grade", type=int)
    parser.add_argument("--student-id", type=int)
    parser.add_argument("--subject-id", type=int)
    parser.add_argument("--date-received")
    return parser.parse_args()


def main():
    args = parse_args()
    session = SessionLocal()
    try:
        payload = get_payload(args, args.model)
        if args.action == "create":
            entity = create_entity(session, args.model, payload)
            print(format_entity(entity))
        elif args.action == "list":
            entities = list_entities(session, args.model)
            for entity in entities:
                print(format_entity(entity))
        elif args.action == "update":
            if args.id is None:
                raise ValueError("id is required for update action")
            entity = update_entity(session, args.model, args.id, payload)
            print(format_entity(entity) if entity else "Record not found")
        elif args.action == "remove":
            if args.id is None:
                raise ValueError("id is required for remove action")
            removed = remove_entity(session, args.model, args.id)
            print("Record removed" if removed else "Record not found")
    except Exception as error:
        session.rollback()
        print(f"Error: {error}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
