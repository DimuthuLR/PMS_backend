from app import create_app, db
from app.models.user import User
from app.utils.auth import hash_password

app = create_app()
with app.app_context():
    # Delete all users first (optional)
    # User.query.delete()
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=hash_password('admin123'),
            role='admin'
        )
        db.session.add(admin)
    
    manager = User.query.filter_by(username='manager').first()
    if not manager:
        manager = User(
            username='manager',
            email='manager@example.com',
            password_hash=hash_password('manager123'),
            role='manager'
        )
        db.session.add(manager)
    
    worker = User.query.filter_by(username='worker').first()
    if not worker:
        worker = User(
            username='worker',
            email='worker@example.com',
            password_hash=hash_password('worker123'),
            role='worker'
        )
        db.session.add(worker)
    
    db.session.commit()
    print("✅ Users created successfully!")
    print("   admin / admin123 (Admin)")
    print("   manager / manager123 (Manager)")
    print("   worker / worker123 (Worker)")