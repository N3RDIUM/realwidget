from flask import Flask, render_template
from flask_socketio import SocketIO
import hyprland
import asyncio
import json, subprocess

hypr = hyprland.Events()

@hypr.on("activewindow")
async def focus_change(*_):
    data = subprocess.check_output("hyprctl activeworkspace -j", shell=True, text=True)
    data = json.loads(data)
    socketio.emit('workspace', data)

@hypr.on("workspace")
async def focus_change_empty(*_):
    data = subprocess.check_output("hyprctl activeworkspace -j", shell=True, text=True)
    data = json.loads(data)
    socketio.emit('workspace', data)

app = Flask(__name__)
socketio = SocketIO(app)

def start_hyprlistener():
    async def run():
        print(hyprland.fetch_workspaces())
        await hypr.async_connect()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    config = hyprland.config.Default()

    socketio.start_background_task(start_hyprlistener)
    socketio.run(app, host="0.0.0.0", port=5000)

