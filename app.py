import os
from game import engine
from flask import Flask, render_template, request, redirect, session

# Load content form the json file.
CONTENT = engine.load_content("game/content.json")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

@app.route("/")
def index():
    """Home Page of the Game"""
    return render_template("index.html")

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/exit", methods=["GET", "POST"])
def exit_game():
    # Clear all game state from session
    session.clear()
    return redirect("/")

@app.route("/howto", methods=["GET"])
def howto():
    """Takes you to playing instructions"""
    return render_template("howto.html")

@app.route("/start", methods=["POST"])
def start():
    """Starts the Game"""
    global CONTENT
    CONTENT = engine.load_content("game/content.json")
    state = engine.new_state(CONTENT)
    session["state"] = state
    return redirect("/play")

@app.route("/command", methods=["POST"])
def command():
    command_text = request.form.get("command", "")
    state = session["state"]
    session["state"] = engine.parse_and_apply(state,command_text, CONTENT)
    return redirect("/play")

@app.route("/play", methods=["GET"])
def play():
    if not session.get("state"):
        return redirect("/")
    state = session["state"]
    room_name = state["current_room"]
    room_description = state["room_description"]
    inventory = state["inventory"]
    messages = state["messages"]

    if room_name in ["arrow_gallery", "pit_of_teeth", "miasma_vault"]:
        return render_template("gameover.html",room_name=room_name,
                                room_description=room_description,
                                inventory=inventory,
                                messages=messages)
    elif room_name == "treasure_chamber":
        return render_template("win.html",room_name=room_name,
                                room_description=room_description,
                                inventory=inventory,
                                messages=messages)
    else:
        return render_template("play.html",
                                room_name=room_name,
                                room_description=room_description,
                                inventory=inventory,
                                messages=messages)