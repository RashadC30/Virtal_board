from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "syncboard-secret-key"
socketio = SocketIO(app, cors_allowed_origins="*")

# Store stroke history in memorry so new users see the current board
stroke_history = []

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    # Send existing canvas strokes to the newly connected client
    emit("load_history", stroke_history)
    
@socketio.on("draw_stroke")
def handle_draw_stroke(data):
    # Recieve a line segment, save it, and broadcast to all other clients
    stroke_history.append(data)
    emit("draw_stroke", data, broadcast=True, include_self=False)

@socketio.on("clear_board")
def handle_clear_board():
    # Clear the stroke history and broadcast the clear event to all clients
    stroke_history.clear()
    emit("clear_board", broadcast=True)
    
if __name__ == "__main__":
    socketio.run(app, debug=True)    