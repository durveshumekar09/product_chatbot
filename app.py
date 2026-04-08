from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Product database
PRODUCTS = {
    "laptop": [
        {"name": "HP Pavilion 14", "price": 55000, "desc": "Good performance, light weight"},
        {"name": "Dell Inspiron 15", "price": 65000, "desc": "Reliable, good display"},
        {"name": "MacBook Air M1", "price": 80000, "desc": "Great battery, best for creators"},
        {"name": "MacBook Air M2", "price": 90000, "desc": "Best for editing, premium build"}
    ],
    "phone": [
        {"name": "Redmi Note 13", "price": 15000, "desc": "Best budget phone"},
        {"name": "Samsung Galaxy A34", "price": 25000, "desc": "Good camera, AMOLED"},
        {"name": "iPhone 12", "price": 42000, "desc": "Premium performance"},
        {"name": "iPhone 13", "price": 52000, "desc": "Great camera and battery"}
    ]
}

# Session state for conversation flow
session_state = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower()

    # Initialize step
    if "step" not in session_state:
        session_state["step"] = 1

    step = session_state["step"]

    # Step 1: Ask category
    if step == 1:
        session_state["step"] = 2
        return jsonify({"response": "Sure! What product do you want to explore? (phone / laptop)"})

    # Step 2: Validate category
    if step == 2:
        if user_msg not in ["phone", "laptop"]:
            return jsonify({"response": "Please choose either *phone* or *laptop*."})
        session_state["category"] = user_msg
        session_state["step"] = 3
        return jsonify({"response": "Nice! What's your budget? (Example: 45000)"})

    # Step 3: Ask budget
    if step == 3:
        if not user_msg.isdigit():
            return jsonify({"response": "Please enter a valid number for the budget."})

        budget = int(user_msg)
        session_state["budget"] = budget
        category = session_state["category"]

        # Filter products within budget
        available = [p for p in PRODUCTS[category] if p["price"] <= budget]

        if not available:
            return jsonify({"response": f"Sorry 😕 No {category} fits within ₹{budget}. Try increasing your budget!"})

        # Recommend highest price within budget
        best = sorted(available, key=lambda x: x["price"], reverse=True)[0]
        session_state["recommended"] = available
        session_state["step"] = 4

        reply = (f"Based on your budget ₹{budget}, I recommend:\n\n"
                 f"**{best['name']}**\n"
                 f"💰 Price: ₹{best['price']}\n"
                 f"⭐ {best['desc']}\n\n"
                 "Would you like another suggestion? (yes/no)")
        return jsonify({"response": reply})

    # Step 4: Offer more suggestions
    if step == 4:
        if user_msg not in ["yes", "no"]:
            return jsonify({"response": "Please reply with yes or no."})

        if user_msg == "no":
            session_state.clear()
            return jsonify({"response": "Great! Happy to help 😊"})

        # Give next product if available
        rec = session_state["recommended"]
        if len(rec) > 1:
            rec.pop(0)
            next_best = rec[0]
            return jsonify({"response": f"Another option:\n\n**{next_best['name']}**\n💰 Price: ₹{next_best['price']}\n⭐ {next_best['desc']}\n\nWant more? (yes/no)"})
        else:
            return jsonify({"response": "No more products under this budget 😊"})

    return jsonify({"response": "Something went wrong. Let's start over!"})

if __name__ == "__main__":
    app.run(debug=True)