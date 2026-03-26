from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_routes():
    with open("routes.json", "r", encoding="utf-8") as file:
        return json.load(file)

def get_locations(routes):
    return sorted(list(set(
        [route["start"] for route in routes] + [route["destination"] for route in routes]
    )))

@app.route("/")
def home():
    routes = load_routes()
    locations = get_locations(routes)
    return render_template(
        "index.html",
        locations=locations,
        results=None,
        selected_start="",
        selected_destination=""
    )

@app.route("/search", methods=["POST"])
def search():
    start = request.form.get("start", "").strip().lower()
    destination = request.form.get("destination", "").strip().lower()

    routes = load_routes()
    locations = get_locations(routes)

    matches = []
    for route in routes:
        if route["start"].lower() == start and route["destination"].lower() == destination:
            matches.append(route)

    return render_template(
        "index.html",
        locations=locations,
        results=matches,
        selected_start=start,
        selected_destination=destination
    )

@app.route("/routes")
def routes_page():
    routes = load_routes()
    return render_template("routes.html", routes=routes)

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    reply = None
    user_message = ""

    if request.method == "POST":
        user_message = request.form.get("message", "")
        if "fare" in user_message.lower():
            reply = "Fares depend on route and transport type. Please check the routes page for sample prices."
        elif "delay" in user_message.lower():
            reply = "Current sample alert: Bus 2 to Robert Gordon University is delayed by 10 minutes."
        elif "airport" in user_message.lower():
            reply = "There is a sample route from Aberdeen to Airport at 11:00 for £4.50."
        else:
            reply = "Thanks for your message. This is a starter AI chatbot page and you can later connect it to a real AI API."

    return render_template("chatbot.html", reply=reply, user_message=user_message)

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    submitted = False
    if request.method == "POST":
        submitted = True
    return render_template("feedback.html", submitted=submitted)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST":
        message = "Login feature UI complete. You can connect this to a real database later."
    return render_template("login.html", message=message)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = None
    if request.method == "POST":
        message = "Sign-up feature UI complete. You can connect this to a real database later."
    return render_template("signup.html", message=message)

@app.route("/route/<int:route_id>")
def route_detail(route_id):
    routes = load_routes()
    selected_route = None

    for route in routes:
        if route["id"] == route_id:
            selected_route = route
            break

    if selected_route is None:
        return "Route not found", 404

    return render_template("route_detail.html", route=selected_route)

if __name__ == "__main__":
    app.run(debug=True)
