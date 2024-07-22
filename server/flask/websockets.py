from flask_socketio import SocketIO, emit, disconnect
from datetime import datetime, timedelta
import asyncio
from config import socketio, app
from flask import request

connected_clients = {}
draft_timers = {}

@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    connected_clients[user_id] = request.sid
    emit('response', {'message': 'Connected to WebSocket server'})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.args.get('user_id')
    if user_id in connected_clients:
        del connected_clients[user_id]

async def start_draft_timer(user_id: str, pick_duration: int):
    end_time = datetime.now() + timedelta(seconds=pick_duration)
    while True:
        now = datetime.now()
        if now >= end_time:
            await notify_user_pick_timeout(user_id)
            break
        else:
            time_left = (end_time - now).total_seconds()
            await notify_user_time_remaining(user_id, time_left)
        await asyncio.sleep(60)  # Check every minute

async def notify_user_pick_timeout(user_id: str):
    if user_id in connected_clients:
        socketio.emit('timeout', {'message': 'Your time to pick has expired!'}, room=connected_clients[user_id])

async def notify_user_time_remaining(user_id: str, time_left: float):
    if user_id in connected_clients:
        socketio.emit('time_remaining', {'time_left': time_left}, room=connected_clients[user_id])

@app.route("/start_draft_timer/", methods=['POST'])
def start_timer():
    user_id = request.json.get('user_id')
    pick_duration = request.json.get('pick_duration')
    if user_id and pick_duration:
        asyncio.create_task(start_draft_timer(user_id, pick_duration))
        return {"message": "Draft timer started"}, 200
    return {"message": "Invalid request"}, 400

@app.route("/stop_draft_timer/", methods=['POST'])
def stop_timer():
    user_id = request.json.get('user_id')
    if user_id and user_id in draft_timers:
        draft_timers[user_id].cancel()
        del draft_timers[user_id]
        return {"message": "Draft timer stopped"}, 200
    return {"message": "Invalid request or no timer found"}, 400

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5555, debug=True)