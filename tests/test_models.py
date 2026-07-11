import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db import Base
from models import Grade, Group, Student, Subject, Teacher


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


def test_student_belongs_to_group(session):
    group = Group(name="AD-101")
    student = Student(name="John Doe", group=group)

    session.add(group)
    session.add(student)
    session.commit()
    session.refresh(student)

    assert student.id is not None
    assert student.group_id == group.id
    assert student.group.name == "AD-101"
