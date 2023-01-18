import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
messages = [
    {
        "name": "Jack",
        "text": "Привет всем, я Jack",
        "time": 1614887855.3456457,
    },
    {
        "name": "Mary",
        "text": "Привет Jack, я - Mary",
        "time": 1614887857.3456457,
    },
]


@app.route("/")
def hello():
    return "<b>Hello, World!</b>"


@app.route("/status")
def page2():
    dt = datetime.now()
    return {
        "status": True,
        "name": "👽 Messenger",
        "time": time.time(),
        "time1": time.asctime(),
        "time2": dt,
        "time3": str(dt),
        "time4": dt.isoformat(),
        "time5": dt.strftime("%d %b %H:%M:%S"),
    }


@app.route("/send", methods=["POST"])
def send_message():
    data = request.json

    name = data.get("name")
    text = data.get("text")

    if not name:
        return abort(400)

    if not text or len(text) > 1000:
        return abort(400)

    message = {"name": name, "text": text, "time": time.time()}
    messages.append(message)

    return {"ok": True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args["after"])
    except:
        return abort(400)

    response = []
    for message in messages:
        if message["time"] > after:
            response.append(message)

    return {"messages": response[:50]}


app.run()
