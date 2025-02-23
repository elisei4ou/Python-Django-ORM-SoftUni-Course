import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student
# Run and print your queries

def add_students():

    student_1 = Student(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )
    student_2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student_3 = Student(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )
    student_4 = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )

    Student.objects.bulk_create([student_1, student_2, student_3, student_4])


def get_students_info():
    return "\n".join([f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}"
                      for s in Student.objects.all()])


def update_students_emails():
    students = Student.objects.all()
    for s in students:
        s.email = s.email.replace('university.com', 'uni-students.com')

    Student.objects.bulk_update(students, ['email'])


def truncate_students():
    Student.objects.all().delete()