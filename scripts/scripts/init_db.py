from app import db, User, MenuItem, Order, Feedback

db.create_all()

# Optionally, you can add a default admin user and some menu items
if not User.query.filter_by(username='admin').first():
    admin_user = User(username='admin', password='your_admin_password')
    db.session.add(admin_user)
    db.session.commit()
