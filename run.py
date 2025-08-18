import os
from dotenv import load_dotenv
from app import create_app
from app.extensions import db
from app.models import User, Task, TaskCategory



# Load environment variables
load_dotenv()

app = create_app()



def create_tables():
    """Create database tables and add default admin user if it doesn't exist"""
    with app.app_context():
        # Only create tables if they don't exist
        db.create_all()

        # Create default admin user if no users exist
        if not User.query.first():
            admin_user = User(
                username='admin',
                email='admin@todoapp.com',
                first_name='Admin',
                last_name='User'
            )
            admin_user.set_password('admin123')
            admin_user.is_active = True

            try:
                db.session.add(admin_user)
                db.session.commit()
                print("Default admin user created: username='admin', password='admin123'")
                
                # Create default categories for admin user
                default_categories = [
                    {'name': 'Work', 'color': '#dc3545'},
                    {'name': 'Personal', 'color': '#28a745'},
                    {'name': 'Shopping', 'color': '#ffc107'},
                    {'name': 'Health', 'color': '#17a2b8'},
                    {'name': 'Learning', 'color': '#6f42c1'}
                ]
                
                for cat_data in default_categories:
                    category = TaskCategory(
                        name=cat_data['name'],
                        color=cat_data['color'],
                        user_id=admin_user.id
                    )
                    db.session.add(category)
                
                db.session.commit()
                print("Default categories created for admin user")
                
            except Exception as e:
                print(f"Error creating admin user: {e}")
                db.session.rollback()

# Create tables and admin user on startup
with app.app_context():
    create_tables()

@app.context_processor
def inject_now():
    """Inject current datetime into templates"""
    from datetime import datetime
    return {'now': datetime.utcnow()}

if __name__ == "__main__":
    # Development server
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting Professional TODO App...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'production')}")
    print(f"Debug mode: {debug_mode}")
    print(f"Server: http://{host}:{port}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        use_reloader=debug_mode
    )

