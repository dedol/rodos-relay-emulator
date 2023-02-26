from dataclasses import asdict

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

from config import Config

from auth import auth_required
from rodos import Rodos

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

CORS(app)

rodos = Rodos(socketio, scheduler, channels=2)

@app.route('/rb<int:id>n.cgi')
def turn_on(id):
    rodos.set_state(id, 'ON')
    return 'Success!'


@app.route('/rb<int:id>f.cgi')
def turn_off(id):
    rodos.set_state(id, 'OFF')
    return 'Success!'


@app.route('/rb<int:id>s.cgi')
def set_timer(id):
    rodos.set_timer(id, app.config['IMPULSE_TIMER_SEC'])
    return 'Success!'


@app.route('/protect/rb<int:id>n.cgi')
@auth_required
def protected_turn_on(id):
    rodos.set_state(id, 'ON')
    return 'Success!'


@app.route('/protect/rb<int:id>f.cgi')
@auth_required
def protected_turn_off(id):
    rodos.set_state(id, 'OFF')
    return 'Success!'


@app.route('/protect/rb<int:id>s.cgi')
@auth_required
def protected_set_timer(id):
    rodos.set_timer(id, app.config['IMPULSE_TIMER_SEC'])
    return 'Success!'


@app.route('/pstat.xml')
def get_states_xml():
    xml = rodos.get_states_xml()
    return xml, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@socketio.on('states')
def get_states(payload):
    for state in rodos.get_states():
        socketio.emit('update', data=asdict(state))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, use_reloader=True, debug=True)
