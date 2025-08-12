# Professional TODO Application

A modern, feature-rich, and production-ready TODO application built with Flask, featuring user authentication, task management, categories, and a RESTful API.

## 🚀 Features

### Core Functionality
- **User Authentication & Authorization**
  - Secure user registration and login
  - Password hashing with Werkzeug
  - Session management with Flask-Login
  - User profiles and password management

- **Advanced Task Management**
  - Create, edit, delete, and toggle tasks
  - Priority levels (Low, Medium, High, Urgent)
  - Task statuses (Pending, In Progress, Completed, Cancelled)
  - Due dates with overdue notifications
  - Task descriptions and categories

- **Category System**
  - Custom task categories with color coding
  - User-specific categories
  - Visual organization of tasks

- **Dashboard & Analytics**
  - Real-time task statistics
  - Visual progress indicators
  - Overdue task alerts
  - Task filtering and sorting

### Technical Features
- **RESTful API**
  - Complete CRUD operations for tasks
  - JSON-based communication
  - API rate limiting
  - CORS support

- **Modern UI/UX**
  - Responsive Bootstrap 5 design
  - Font Awesome icons
  - Interactive modals and forms
  - Real-time updates

- **Security & Performance**
  - CSRF protection
  - SQL injection prevention
  - Secure session handling
  - Database optimization

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.3** - Modern Python web framework
- **Flask-SQLAlchemy 3.1.1** - Database ORM
- **Flask-Login 0.6.3** - User session management
- **Flask-Migrate 4.0.5** - Database migrations
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **SQLAlchemy 2.0+** - Database toolkit

### Frontend
- **Bootstrap 5.3.0** - Responsive CSS framework
- **Font Awesome 6.4.0** - Icon library
- **Vanilla JavaScript** - Modern ES6+ features
- **HTML5 & CSS3** - Semantic markup and styling

### Database
- **SQLite** (Development) - Lightweight database
- **PostgreSQL/MySQL** (Production) - Enterprise databases

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd TODO_APP
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```bash
# Copy the example configuration
cp .env.example .env

# Edit the .env file with your settings
FLASK_ENV=development
SECRET_KEY=your-super-secret-key
DATABASE_URL=sqlite:///todo.db
```

### 5. Initialize Database
```bash
# The database will be created automatically on first run
# Default admin user: admin/admin123
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`

## 🔐 Default Credentials

- **Username:** `admin`
- **Password:** `admin123`

**⚠️ Important:** Change these credentials immediately after first login in production!

## 📱 Usage

### Getting Started
1. **Register/Login**: Create a new account or use the default admin credentials
2. **Dashboard**: View your task overview and statistics
3. **Add Tasks**: Use the "Add Task" button to create new tasks
4. **Organize**: Create categories and assign priorities to tasks
5. **Track Progress**: Update task statuses as you work on them

### Task Management
- **Create**: Add new tasks with title, description, priority, and due date
- **Edit**: Modify existing tasks anytime
- **Toggle**: Quickly change task status (Pending → In Progress → Completed)
- **Delete**: Remove completed or unnecessary tasks
- **Filter**: View tasks by status, priority, or category

### Categories
- **Create**: Add custom categories with color coding
- **Organize**: Group related tasks under categories
- **Visual**: Use colors to quickly identify task types

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Application environment | `production` |
| `SECRET_KEY` | Flask secret key | Required in production |
| `DATABASE_URL` | Database connection string | `sqlite:///todo.db` |
| `HOST` | Server host | `127.0.0.1` |
| `PORT` | Server port | `5000` |

### Production Deployment
1. Set `FLASK_ENV=production`
2. Configure a strong `SECRET_KEY`
3. Use a production database (PostgreSQL/MySQL)
4. Set up HTTPS with proper SSL certificates
5. Configure reverse proxy (Nginx/Apache)
6. Use Gunicorn or uWSGI as WSGI server

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `first_name`, `last_name`: User details
- `is_active`: Account status
- `created_at`, `last_login`: Timestamps

### Tasks Table
- `id`: Primary key
- `title`: Task title
- `description`: Task description
- `status`: Current status
- `priority`: Priority level
- `due_date`: Due date
- `user_id`: Foreign key to users
- `category_id`: Foreign key to categories
- `created_at`, `updated_at`, `completed_at`: Timestamps

### Categories Table
- `id`: Primary key
- `name`: Category name
- `color`: Hex color code
- `user_id`: Foreign key to users
- `created_at`: Timestamp

## 🚀 API Endpoints

### Authentication Required
All API endpoints require authentication via Flask-Login.

### Tasks
- `GET /api/tasks` - Get all tasks (with optional filters)
- `GET /api/tasks/<id>` - Get specific task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `POST /api/tasks/<id>/toggle` - Toggle task status

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create new category

### Statistics
- `GET /api/stats` - Get task statistics

## 🧪 Testing

### Run Tests
```bash
# Set testing environment
export FLASK_ENV=testing

# Run tests
python -m pytest tests/
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run -m pytest
coverage report
coverage html
```

## 🔒 Security Features

- **Password Security**: Bcrypt hashing with salt
- **Session Management**: Secure session handling
- **CSRF Protection**: Cross-site request forgery prevention
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Output escaping and sanitization

## 📊 Performance Optimization

- **Database Indexing**: Optimized queries with proper indexes
- **Lazy Loading**: Efficient relationship loading
- **Caching**: Session and data caching strategies
- **Pagination**: Large dataset handling
- **API Rate Limiting**: Prevent abuse

## 🚀 Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Environment Variables for Production
```bash
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/todo_db
HOST=0.0.0.0
PORT=5000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🔮 Future Enhancements

- **Email Notifications**: Due date reminders and updates
- **File Attachments**: Attach files to tasks
- **Team Collaboration**: Share tasks and assign to team members
- **Mobile App**: Native mobile applications
- **Advanced Analytics**: Detailed progress tracking and reports
- **Integration**: Connect with external tools (Slack, Trello, etc.)
- **Offline Support**: Progressive Web App features

---

**Built with ❤️ using Flask and modern web technologies**
#   T o - D o - L i s t - a p p  
 