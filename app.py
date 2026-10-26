from flask import Flask, request, jsonify

app = Flask(__name__)
students = {}
next_id = 1


@app.route("/")
def home():
    return "Student API is running!"


@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(list(students.values()))


@app.route("/students", methods=["POST"])
def add_student():
    global next_id
    data = request.json
    data["id"] = next_id
    students[next_id] = data
    next_id += 1
    return jsonify(data), 201


@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(students[id])


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404
    students[id].update(request.json)
    students[id]["id"] = id
    return jsonify(students[id])


@app.route("/students/<int:id>", methods=["PATCH"])
def patch_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404
    students[id].update(request.json)
    return jsonify(students[id])


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404
    del students[id]
    return jsonify({"message": "Student deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
