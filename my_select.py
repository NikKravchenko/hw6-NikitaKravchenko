from sqlalchemy import desc, func

from db import SessionLocal
from models import Grade, Group, Student, Subject, Teacher

session = SessionLocal()


def select_1():
    return (
        session.query(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(subject_id):
    return (
        session.query(
            Student.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    )


def select_3(subject_id):
    return (
        session.query(
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


def select_4():
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()


def select_5(teacher_id):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


def select_6(group_id):
    return session.query(Student.name).filter(Student.group_id == group_id).all()


def select_7(group_id, subject_id):
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


def select_8(teacher_id):
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


def select_9(student_id):
    return (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )


def select_10(student_id, teacher_id):
    return (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )


def select_11(teacher_id, student_id):
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )


def select_12(group_id, subject_id):
    max_date_subquery = (
        session.query(func.max(Grade.date_received))
        .select_from(Grade)
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar_subquery()
    )
    return (
        session.query(Student.name, Grade.grade, Grade.date_received)
        .select_from(Grade)
        .join(Student)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == max_date_subquery,
        )
        .all()
    )


if __name__ == "__main__":
    first_student = session.query(Student.id).first()
    first_group = session.query(Group.id).first()
    first_subject = session.query(Subject.id).first()
    first_teacher = session.query(Teacher.id).first()

    student_id = first_student[0] if first_student else 1
    group_id = first_group[0] if first_group else 1
    subject_id = first_subject[0] if first_subject else 1
    teacher_id = first_teacher[0] if first_teacher else 1

    print(select_1())
    print(select_2(subject_id))
    print(select_3(subject_id))
    print(select_4())
    print(select_5(teacher_id))
    print(select_6(group_id))
    print(select_7(group_id, subject_id))
    print(select_8(teacher_id))
    print(select_9(student_id))
    print(select_10(student_id, teacher_id))
    print(select_11(teacher_id, student_id))
    print(select_12(group_id, subject_id))
