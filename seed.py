import random
from faker import Faker
from db import SessionLocal
from models import Group, Teacher, Subject, Student, Grade

fake = Faker('uk_UA')

def seed_data():
    session = SessionLocal()
    
    # Очищаємо базу перед новим заповненням (щоб не було дублікатів)
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()
    session.commit()

    # 1. Створюємо 3 групи
    groups = [Group(name=f"Group-{i}") for i in ['A', 'B', 'C']]
    session.add_all(groups)
    session.commit()
    
    # 2. Створюємо 4 викладачів
    teachers = [Teacher(name=fake.name()) for _ in range(4)]
    session.add_all(teachers)
    session.commit()
    
    # 3. Створюємо 6 предметів
    subject_names = ['Математика', 'Фізика', 'Хімія', 'Історія', 'Програмування', 'Англійська']
    subjects = [Subject(name=name, teacher_id=random.choice(teachers).id) for name in subject_names]
    session.add_all(subjects)
    session.commit()
    
    # 4. Створюємо 40 студентів
    students = [Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(40)]
    session.add_all(students)
    session.commit()
    
    # 5. Створюємо оцінки (до 20 для кожного студента)
    grades = []
    for student in students:
        for _ in range(random.randint(10, 20)):
            date_rec = fake.date_between(start_date='-1y', end_date='today')
            grade = Grade(
                grade=random.randint(1, 12),  # Оцінки від 1 до 12
                date_received=date_rec,
                student_id=student.id,
                subject_id=random.choice(subjects).id
            )
            grades.append(grade)
    
    session.add_all(grades)
    session.commit()
    session.close()
    print("Базу даних успішно наповнено!")

if __name__ == '__main__':
    seed_data()