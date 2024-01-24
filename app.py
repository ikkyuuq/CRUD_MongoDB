from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from db import student_collection, major_collection
from models import get_students
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
basic_auth = BasicAuth(app)

app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD')

@app.get('/')
def welcome():
    return jsonify({'message': 'Welcome to Student Management API'})

@app.get('/students/<int:std_id>')
@basic_auth.required
def get_student_by_id(std_id):
    student_data = student_collection.find({'std_id': int(std_id)})
    major_data = list(major_collection.find())
    
    return get_students(student_data, major_data)

@app.get('/students')
@basic_auth.required
def get_all_students():
    student_data = student_collection.find()
    major_data = list(major_collection.find())
    
    return get_students(student_data, major_data)

@app.post('/students')
@basic_auth.required
def create_new_student():
    std_id = request.json['std_id']
    std_fname = request.json['std_fname']
    std_lname = request.json['std_lname']
    major_id = request.json['major_id']
    
    student_data = student_collection.find_one({'std_id': std_id})
    major_data = major_collection.find_one({'major_id': major_id})
    
    if student_data:
        return jsonify({"error":"Cannot create new student"}), 500
    if major_data:
        data = {
            'std_id': std_id,
            'std_fname': std_fname,
            'std_lname': std_lname,
            'major_id': major_id
        }
        student_collection.insert_one(data)
        return jsonify({'message': "Student inserted successfully"}), 200 
    
    return jsonify({'error': f'major_id {major_id} not found!'}), 404

@app.put('/students/<int:std_id>')
@basic_auth.required
def update_student(std_id):
    existing_student = student_collection.find_one({'std_id': std_id})
    new_std_id = request.json.get('std_id')
    new_std_fname = request.json.get('std_fname')
    new_std_lname = request.json.get('std_lname')
    new_major_id = request.json.get('major_id')
    
    update_query = {
        '$set': {
            'std_id': new_std_id,
            'std_fname': new_std_fname,
            'std_lname': new_std_lname,
            'major_id': new_major_id
        }
    }
    
    if existing_student is None:
        return jsonify({"error": "Student not found"}), 404

    new_student_data = student_collection.find_one({'std_id': new_std_id})
    if new_student_data == existing_student:
        major_data = major_collection.find_one({'major_id': new_major_id})
        if not major_data:
            return jsonify({'error': f'major_id {new_major_id} not found!'}), 404
    
        student_collection.update_one({'std_id': std_id}, update_query)
        return jsonify({'message': "Student updated successfully"}), 200
    elif new_student_data != existing_student:
        if new_student_data:
            return jsonify({"error": f"std_id {new_std_id} is exists"}), 409
        major_data = major_collection.find_one({'major_id': new_major_id})
        if not major_data:
            return jsonify({'error': f'major_id {new_major_id} not found!'}), 404
    
        student_collection.update_one({'std_id': std_id}, update_query)
        return jsonify({'message': "Student updated successfully"}), 200
    


@app.delete('/students/<int:std_id>')
@basic_auth.required
def delete_student_by_id(std_id):
    student_data = student_collection.find_one({'std_id': int(std_id)})
    if student_data is None:
        return jsonify({"error": "Student not found"}), 404
    
    student_collection.delete_one({'std_id': int(std_id)})
    return jsonify({'message': "Student deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)