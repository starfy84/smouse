
from flask import Flask, request
from flask_socketio import SocketIO,emit
import win32api, win32con
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)
socketio = SocketIO(app)

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

device: dict[str, tuple[float,float,float,float,float,float,int]] = {}
dd = []

def trapezoid(a, pa, dt):
    return pa + (a + pa) / 2 * dt

@socketio.on('connect')
def connect():
    print('connect ', request.sid)

@socketio.on('disconnect')
def disconnect():
    print('disconnect')

@socketio.on('show')
def show(sid):
    d = np.array(dd[-500:])
    y = np.arange(0, len(d))
    plt.plot(y,d)
    plt.show()

@socketio.on('data')
def data(ax,ay,az,ts):
    if device.get(request.sid, None) is None:
        device[request.sid] = (ax, ay, az, 0, 0, 0, ts)

    (pax, pay, paz, pvx, pvy, pvz, pts) = device[request.sid]

    dt = (ts-pts)/1e9
    
    vx = trapezoid(ax, pax, dt)
    vy = trapezoid(ay, pay, dt)
    vz = trapezoid(az, paz, dt)

    dx = vx*dt
    dy = vy*dt
    dz = vz*dt

    print(f'{vx} {vy}', end='\r')

    move_mouse(dx, -dy, 1e3)

    device[request.sid] = (ax, ay, az, vx, vy, vz, ts)
    dd.append(vx)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def move_mouse(dx, dy, multiplier = 1):
    # win32api.SetCursorPos(int(dx),int(dy))
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(dx*multiplier),int(dy*multiplier),0,0)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0",debug=True,port=5001)
