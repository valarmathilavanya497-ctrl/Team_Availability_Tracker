from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "team_data.json"

DEFAULT_TEAM = [
    {"id": 1, "name": "Alex Rivers", "role": "Senior Developer", "available": True},
    {"id": 2, "name": "Samantha Chen", "role": "UX Designer", "available": False},
    {"id": 3, "name": "Jordan Taylor", "role": "Project Manager", "available": True},
    {"id": 4, "name": "Maria Garcia", "role": "Marketing Lead", "available": True},
    {"id": 5, "name": "David Kim", "role": "Backend Engineer", "available": False},
    {"id": 6, "name": "Priya Sharma", "role": "Data Analyst", "available": True},
]

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    save_db(DEFAULT_TEAM)
    return DEFAULT_TEAM

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/api/team", methods=["GET"])
def get_team():
    team = load_db()
    return jsonify({"success": True, "team": team})

@app.route("/api/team/<int:member_id>/availability", methods=["PATCH"])
def update_availability(member_id):
    data = request.get_json()
    if "available" not in data:
        return jsonify({"success": False, "error": "Missing 'available' field"}), 400

    team = load_db()
    for member in team:
        if member["id"] == member_id:
            member["available"] = bool(data["available"])
            save_db(team)
            return jsonify({"success": True, "member": member})

    return jsonify({"success": False, "error": "Member not found"}), 404

@app.route("/api/team", methods=["POST"])
def add_member():
    data = request.get_json()
    if not data.get("name") or not data.get("role"):
        return jsonify({"success": False, "error": "Name and role are required"}), 400

    team = load_db()
    new_id = max((m["id"] for m in team), default=0) + 1
    new_member = {
        "id": new_id,
        "name": data["name"],
        "role": data["role"],
        "available": data.get("available", True)
    }
    team.append(new_member)
    save_db(team)
    return jsonify({"success": True, "member": new_member}), 201

@app.route("/api/team/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    team = load_db()
    updated = [m for m in team if m["id"] != member_id]
    if len(updated) == len(team):
        return jsonify({"success": False, "error": "Member not found"}), 404
    save_db(updated)
    return jsonify({"success": True})

if __name__ == "__main__":
    print("Server running at http://localhost:5000")
    app.run(debug=True, port=5000)