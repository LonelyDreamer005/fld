from flask import Flask, request, jsonify

app = Flask(__name__)

students = {}
next_id = 1


# Home
@app.route("/")
def home():
    return "Student API is running!"


# READ: Get all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(list(students.values()))


# CREATE: Add a student
@app.route("/students", methods=["POST"])
def add_student():
    global next_id

    data = request.get_json()

    student = {
        "id": next_id,
        "name": data["name"],
        "course": data["course"]
    }

    students[next_id] = student
    next_id += 1

    return jsonify(student), 201


# READ: Get one student
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(students[id])


# UPDATE: Update a student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    students[id]["name"] = data["name"]
    students[id]["course"] = data["course"]

    return jsonify(students[id])

@app.route("/students/<int:id>", methods=["PATCH"])
def update_students(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in data:
        students[id]["name"] = data["name"]

    if "course" in data:
        students[id]["course"] = data["course"]

    return jsonify(students[id]), 200


# DELETE: Delete a student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    del students[id]

    return jsonify({"message": "Student deleted"})


if __name__ == "__main__":
    app.run(host ="0.0.0.0", port = 5000)
