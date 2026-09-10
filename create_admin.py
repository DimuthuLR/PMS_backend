from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Check if admin already exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user 'admin' with password 'admin123' created!")
    else:
        print("ℹ️ Admin user already exists.")