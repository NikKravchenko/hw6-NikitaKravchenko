import argparse

from db import Base, SessionLocal, engine
from models import Group, Student, Subject, Teacher


MODEL_MAP = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
}


def create_entity(session, model_name, name):
    model = MODEL_MAP[model_name]
    if model_name == "Student":
        entity = model(name=name, group_id=1)
    elif model_name == "Subject":
        entity = model(name=name, teacher_id=1)
    else:
        entity = model(name=name)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity


def list_entities(session, model_name):
    model = MODEL_MAP[model_name]
    return session.query(model).order_by(model.id).all()


def update_entity(session, model_name, entity_id, name):
    model = MODEL_MAP[model_name]
    entity = session.query(model).filter(model.id == entity_id).first()
    if not entity:
        return None
    entity.name = name
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"])
    parser.add_argument("-m", "--model", required=True, choices=["Teacher", "Group", "Student", "Subject"])
    parser.add_argument("-n", "--name")
    parser.add_argument("--id", type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        if args.action == "create":
            if not args.name:
                raise ValueError("name is required for create action")
            entity = create_entity(session, args.model, args.name)
            print(entity.id, entity.name)
        elif args.action == "list":
            entities = list_entities(session, args.model)
            for entity in entities:
                print(entity.id, entity.name)
        elif args.action == "update":
            if args.id is None or not args.name:
                raise ValueError("id and name are required for update action")
            entity = update_entity(session, args.model, args.id, args.name)
            if entity:
                print(entity.id, entity.name)
            else:
                print("Record not found")
        elif args.action == "remove":
            if args.id is None:
                raise ValueError("id is required for remove action")
            removed = remove_entity(session, args.model, args.id)
            if removed:
                print("Record removed")
            else:
                print("Record not found")
    except Exception as error:
        session.rollback()
        print(f"Error: {error}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
