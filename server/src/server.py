
from flask import Flask, request
from flask_socketio import SocketIO,emit
import win32api, win32con


app = Flask(__name__)
socketio = SocketIO(app)

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

device: dict[str, tuple[float,float,float,float,float,float,int]] = {}

i_vel_x = 0
i_vel_y = 0
v_thresh = 0.1
a_thresh = 0.1


def trapezoid(a, pa, dt):
    return pa + (a + pa) / 2 * dt

@socketio.on('connect')
def connect():
    print('connect ', request.sid)

@socketio.on('disconnect')
def disconnect():
    print('disconnect')

@socketio.on('data')
def data(ax,ay,az,ts):
    global i_vel_x, i_vel_y
    if device.get(request.sid, None) is None:
        device[request.sid] = (ax, ay, az, 0, 0, 0, ts)

    (pax, pay, paz, pvx, pvy, pvz, pts) = device[request.sid]

    dt = (ts-pts)/1e9

    if abs(ax) < a_thresh:
        ax = 0
    if abs(ay) < a_thresh:
        ay = 0
    
    vx = trapezoid(ax, pax, dt)
    vy = trapezoid(ay, pay, dt)
    vz = trapezoid(az, paz, dt)

    if abs(vx) < v_thresh:
        vx = 0
    if abs(vy) < v_thresh:
        vy = 0


    if ax == 0 and vx == 0:
        i_vel_x = 0

    if ay == 0 and vy == 0:
        i_vel_y = 0        


    i_vel_x += vx
    i_vel_y += vy

    dx = vx*dt
    dy = vy*dt
    dz = vz*dt

    print(f'{ax:.1f} {ay:.1f}', end='\r')

    if az < a_thresh:
        move_mouse(i_vel_x, -i_vel_y, 1)

    device[request.sid] = (ax, ay, az, vx, vy, vz, ts)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def move_mouse(dx, dy, multiplier = 1):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(dx*multiplier),int(dy*multiplier),0,0)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0",debug=True,port=5001)
