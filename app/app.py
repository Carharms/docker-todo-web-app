# app/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from sqlalchemy import text

# pymysql set as underlying MySQLdriver for SQLAlchemy
pymysql.install_as_MySQLdb()
app = Flask(__name__)

# -- Database Configuration --
# Retrieve MySQL credentials from docker-compose file
DB_USER = os.getenv('MYSQL_USER', 'app-user')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
DB_HOST = os.getenv('MYSQL_HOST', 'db')
DB_PORT = os.getenv('MYSQL_PORT', '3306')
DB_NAME = os.getenv('MYSQL_DATABASE', 'todo_db')

# Sturctures DB connection url
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Disable SQLAlchemy feature that tracks modications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -- Database Model --
class Todo(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.String(50), default='Incomplete')  # Fixed: changed from db.Bool to db.String to match SQL

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed
        }

# -- API Endpoints --

# Dedicated endpoint to check the DB connection with lightweight query
@app.route('/db_healthz')
def db_healthz():
    try:
        db.session.execute(text('SELECT 1')) 
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

# Retrieve all todo_list items 
@app.route('/todo_list', methods=['GET'])
def get_todo_list():
    todo_list = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todo_list])

# Add new to-do item 
@app.route('/todo_list', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Task required'}), 400   
    new_todo = Todo(task=data['task'])
    if 'completed' in data:
        new_todo.completed = data['completed']
    
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# Delete existing to-do item
@app.route('/todo_list/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': f'Todo with ID {todo_id} deleted'}), 200

# -- Health Check Endpoint --
# Checks both app and DB health
@app.route('/healthz', methods=['GET'])
def health_check():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify(status="healthy", database_connection="ok"), 200
    except Exception as e:
        # If exception triggered, the app cannot reach DB
        return jsonify(status="unhealthy", database_connection="failed", error=str(e)), 500

# -- Main execution --
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created/checked by Flask app (after DB healthy).")
    app.run(host='0.0.0.0', port=5000)