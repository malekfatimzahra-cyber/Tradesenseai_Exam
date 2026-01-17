from app import app, db
from models import Course

with app.app_context():
    courses = Course.query.all()
    print(f"Total courses: {len(courses)}")
    for c in courses:
        print(f"ID: {c.id}, Title: {c.title}")
