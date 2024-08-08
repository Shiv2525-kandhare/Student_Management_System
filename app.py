from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/sms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/departments', methods=['GET'])
def get_departments():
    
    result = db.session.execute(text("SELECT * FROM department"))
    departments = [dict(row) for row in result.mappings()] # mappings return column inside table in the form of dictionary instead of tuples which was returned by fetch all
    return jsonify(departments), 200

@app.route('/courses', methods=['GET'])
def get_courses():
    
    result = db.session.execute(text("SELECT * FROM course"))
    courses = [dict(row) for row in result.mappings()] # mappings return column inside table in the form of dictionary instead of tuples which was returned by fetch all
    return jsonify(courses), 200

@app.route('/students', methods=['GET'])
def get_students():
    
    result = db.session.execute(text("SELECT * FROM student"))
    students = [dict(row) for row in result.mappings()] # mappings return column inside table in the form of dictionary instead of tuples which was returned by fetch all
    return jsonify(students), 200

@app.route('/register', methods=['GET','POST'])
def registration_of_student():
    
    if request.method == 'POST':
        student_data = request.get_json()
    
        name = student_data['name']
        age = student_data['age']
        student_class = student_data['class']
        address = student_data['address']
        enrolled_date = student_data['enrolled_date']
        dept_id = student_data['dept_id']
        c_id = student_data['c_id']
        
        count = db.session.execute(
            text("SELECT COUNT(*) FROM course WHERE c_id = :c_id AND dept_id = :dept_id"),
            {"c_id": c_id, "dept_id": dept_id}
        ).scalar()

        if count == 0:
            return jsonify({"error": "The selected course does not belong to the chosen department."}), 400
    
        db.session.execute(
               text("INSERT INTO student (name, age, class, address, enrolled_date, dept_id, c_id) VALUES (:name, :age, :class, :address, :enrolled_date, :dept_id, :c_id)"),
            {"name": name, "age": age, "class": student_class, "address": address, "enrolled_date": enrolled_date, "dept_id": dept_id, "c_id": c_id}
            )
        db.session.commit()
    return jsonify({"message": "Student registered successfully!"}), 201

@app.route('/deletestudents/<int:roll_no>', methods=['DELETE'])
def delete_student(roll_no):
    
    db.session.execute(
            text("DELETE FROM student WHERE roll_no = :roll_no"),
            {"roll_no": roll_no}
        )
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)

