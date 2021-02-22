from flask import Flask, request, url_for, redirect
from flask import render_template
from controller import Remote
import json
app = Flask(__name__)

LEFT, RIGHT, UP, DOWN, HOME, ENTER = "left", "right", "up", "down", "home", "enter"
AVAIALABLE_COMMANDS = {
    'Left'  : LEFT,
    'Right' : RIGHT,
    'Up'    : UP,
    'Down'  : DOWN,
    'Home'  : HOME,
    'Enter' : ENTER
}

with open (r"C:\Users\Chip\Documents\personalProjects\personalProjects\rokuController\tvNameAndIP.txt", 'r') as f:
    json_data = json.load(f)

app = Flask(__name__)

r = Remote()


@app.route('/')
def execute():
    r.scan()
    return render_template('displayTVs.html', tvs = json_data)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    ip = request.form['tv']
    r.ip=ip
    return redirect(url_for('command', cmd="Home"))

@app.route('/commands/<cmd>/')
def command(cmd=None):
    r.pressButton(cmd)
    return render_template("main.html" , commands = AVAIALABLE_COMMANDS)

if __name__ == '__main__':

    app.run(debug=True)


    
