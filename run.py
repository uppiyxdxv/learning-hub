from app import app, db
with app.app_context():
    db.create_all()
print("🚀 Learning Platform running on http://localhost:5000")
app.run(debug=True)
