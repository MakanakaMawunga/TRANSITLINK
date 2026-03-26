from flask import Flask, render_template, request
import json

app = Flask(__name__, template_folder="templates", static_folder="static")

USER_PROFILE = {
    "name": "Guest User",
    "email": "guest@transitlink.com",
    "wheelchair_access": True,
    "step_free": True,
    "audio_announcements": True,
    "priority_seating": True,
    "home_location": "Home",
    "work_location": "Work",
    "school_location": "School",
    "shopping_location": "Union Square"
}

SAVED_ROUTES = [
    {"label": "Home to School", "start": "Home", "destination": "School"},
    {"label": "School to Home", "start": "School", "destination": "Home"},
    {"label": "Home to Shopping", "start": "Home", "destination": "Union Square"}
]


def load_routes():
    with open("routes.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_locations(routes):
    return sorted(list(set([route["start"] for route in routes] + [route["destination"] for route in routes])))


def filter_routes_for_profile(routes):
    filtered = []
    for route in routes:
        if USER_PROFILE["wheelchair_access"] and not route["wheelchair_access"]:
            continue
        if USER_PROFILE["step_free"] and not route["step_free"]:
            continue
        if USER_PROFILE["audio_announcements"] and not route["audio_announcements"]:
            continue
        if USER_PROFILE["priority_seating"] and not route["priority_seating"]:
            continue
        filtered.append(route)
    return filtered


@app.route("/")
def home():
    routes = load_routes()
    locations = get_locations(routes)
    return render_template(
        "index.html",
        locations=locations,
        results=None,
        selected_start="",
        selected_destination="",
        profile=USER_PROFILE
    )


@app.route("/search", methods=["POST"])
def search():
    start = request.form.get("start", "").strip().lower()
    destination = request.form.get("destination", "").strip().lower()

    routes = filter_routes_for_profile(load_routes())
    locations = get_locations(load_routes())

    matches = []
    for route in routes:
        if route["start"].lower() == start and route["destination"].lower() == destination:
            matches.append(route)

    return render_template(
        "index.html",
        locations=locations,
        results=matches,
        selected_start=start,
        selected_destination=destination,
        profile=USER_PROFILE
    )


@app.route("/routes")
def routes_page():
    routes = filter_routes_for_profile(load_routes())
    return render_template("routes.html", routes=routes, profile=USER_PROFILE)


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


@app.route("/profile", methods=["GET", "POST"])
def profile():
    message = None

    if request.method == "POST":
        USER_PROFILE["name"] = request.form.get("name", USER_PROFILE["name"])
        USER_PROFILE["email"] = request.form.get("email", USER_PROFILE["email"])
        USER_PROFILE["wheelchair_access"] = request.form.get("wheelchair_access") == "on"
        USER_PROFILE["step_free"] = request.form.get("step_free") == "on"
        USER_PROFILE["audio_announcements"] = request.form.get("audio_announcements") == "on"
        USER_PROFILE["priority_seating"] = request.form.get("priority_seating") == "on"
        USER_PROFILE["home_location"] = request.form.get("home_location", USER_PROFILE["home_location"])
        USER_PROFILE["work_location"] = request.form.get("work_location", USER_PROFILE["work_location"])
        USER_PROFILE["school_location"] = request.form.get("school_location", USER_PROFILE["school_location"])
        USER_PROFILE["shopping_location"] = request.form.get("shopping_location", USER_PROFILE["shopping_location"])
        message = "Profile updated successfully."

    return render_template("profile.html", profile=USER_PROFILE, message=message)


@app.route("/dashboard")
def dashboard():
    accessible_routes = filter_routes_for_profile(load_routes())
    return render_template(
        "dashboard.html",
        profile=USER_PROFILE,
        saved_routes=SAVED_ROUTES,
        recommended_routes=accessible_routes[:3]
    )


@app.route("/saved-routes")
def saved_routes():
    return render_template("saved_routes.html", saved_routes=SAVED_ROUTES, profile=USER_PROFILE)


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    reply = None
    user_message = ""

    if request.method == "POST":
        user_message = request.form.get("message", "")
        text = user_message.lower()

        if "accessible" in text or "wheelchair" in text:
            reply = "Based on your saved profile, TransitLink is showing routes with accessibility support such as wheelchair access, step-free boarding, audio announcements, and priority seating where available."
        elif "home" in text:
            reply = f"Your saved home location is {USER_PROFILE['home_location']}. You can use the saved routes page to quickly open your frequent journeys."
        elif "school" in text:
            reply = f"Your saved school location is {USER_PROFILE['school_location']}. You can search routes between home and school from the dashboard."
        elif "work" in text:
            reply = f"Your saved work location is {USER_PROFILE['work_location']}."
        elif "shopping" in text:
            reply = f"Your saved shopping location is {USER_PROFILE['shopping_location']}."
        elif "delay" in text:
            reply = "Current example delay: Bus 2 to Robert Gordon University is delayed."
        else:
            reply = "I can help with saved places, accessible routes, delays, and frequent journeys. Try asking about home, work, school, shopping, or accessible travel."

    return render_template("chatbot.html", reply=reply, user_message=user_message, profile=USER_PROFILE)


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


if __name__ == "__main__":
    app.run(debug=True)
