from app import create_app, db, bcrypt
from models import User

app = create_app()

with app.app_context():
    # Check if admin already exists
    if (admin := db.session.query(User).filter_by(email='admin@example.com').first()):
        print("Admin user already exists")
    else:
        # Create admin user
        password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            name='Admin',
            email='admin@example.com',
            password_hash=password_hash,
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
        print("Email: admin@example.com")
        print("Default password: admin123 (change after first login)")