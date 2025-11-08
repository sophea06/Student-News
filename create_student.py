from app import create_app, db, bcrypt
from models import User

app = create_app()

with app.app_context():
    # Check if student already exists
    if (student := db.session.query(User).filter_by(email='student@example.com').first()):
        print("Student user already exists")
    else:
        # Create student user
        password_hash = bcrypt.generate_password_hash('student123').decode('utf-8')
        student = User(
            name='Student',
            email='student@example.com',
            password_hash=password_hash,
            role='student'
        )
        db.session.add(student)
        db.session.commit()
        print("Student user created successfully")
        print("Email: student@example.com")
        print("Default password: student123 (change after first login)")