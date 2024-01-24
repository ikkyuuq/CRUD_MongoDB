from flask import jsonify

def get_students(student_data, major_data):
    results = []
    for std in student_data:
        print(std.get('major_id'))
        major = next((m for m in major_data if m.get('major_id', '') == std.get('major_id', '')), None)
        result = {
            'std_id': std.get('std_id', ''),
            'std_fname': std.get('std_fname', ''),
            'std_lname': std.get('std_lname', ''),
            'major_id': std.get('major_id', ''),
            'major_title': major.get('major_title', '')
        }
        print(major.get('major_title'))
        results.append(result)
        
    return (jsonify({'results': results}), 200) if results else  (jsonify({"error":"Student not found"}), 404)