from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Course, Enrollment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], 
                   email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    available_courses = Course.query.all()
    return render_template('dashboard.html', 
                         enrollments=enrollments, 
                         courses=available_courses)

@app.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).first()
    if not enrollment:
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Enrolled successfully!')
    return jsonify({'success': True})

@app.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Course.query.first():
            courses = [
                # YOUR REQUESTED COURSES
                Course(title='Java Programming', description='Master Java from basics to advanced OOP', price=39.99),
                Course(title='Python ', description=' Python: decorators, generators, async', price=49.99),
                Course(title='C Programming', description='C language fundamentals, pointers, memory management', price=29.99),
                Course(title='Full Stack Web Dev', description='HTML/CSS/JS + Backend (Node/Python) + Database', price=79.99),
                Course(title='Database Mastery', description='SQL, NoSQL, MongoDB, optimization', price=59.99),
                
                # BONUS: Additional popular courses
                Course(title='JavaScript Essentials', description='Modern JavaScript ES6+ with projects', price=34.99),
                Course(title='Node.js Backend', description='Build APIs with Express & MongoDB', price=59.99),
                Course(title='Docker & DevOps', description='Containerization and CI/CD pipelines', price=89.99)
            ]
            for course in courses:
                db.session.add(course)
            db.session.commit()
            print("✅ Database seeded with Java, Python, C, Fullstack, Database + 4 more courses!")
    app.run(debug=True, port=5000)
