from . import main
from flask import jsonify, request

from ..services.grievance_service import register_grievance, handle_grievance


@main.route("/register_grievance", methods=["POST"])
def home():
    user_query = request.json.get("query", "")
    data = register_grievance(user_query)
    print("Data from register_grievance:", data)
    return jsonify(data)

@main.route("/telegram_bot", methods=["POST"])
def bot():
    user_query = request.json.get("query", "")
    data = handle_grievance(user_query)
    print("Data from register_grievance:", data)
    return jsonify(data)
