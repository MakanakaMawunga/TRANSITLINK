from flask import Flask, render_template, request
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

