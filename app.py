from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import date
from utils import export_csv

app = Flask(__name__)

DATA_FILE = 'data.json'

TEAM_MEMBERS = [
    "v-asasane", "v-ayushg", "v-aysaini", "v-bhagpatil", "v-ckendre",
    "v-chevukumar", "v-chintreddy", "v-dvengala", "v-dgadave", "v-gdiwakar",
    "v-krutwik", "v-kotasatya", "v-krshinde", "v-mgire", "v-nrenuka",
    "v-nisbhavsar", "v-deshmukhp", "v-pthengane", "v-yadavprade",
    "v-ragaikwad", "v-rashmsingh", "v-saurabhv", "v-snambissan",
    "v-shwetabais", "v-sshelke", "v-trunwal", "v-ubhuvibhar"
]

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    data = load_data()
    today = date.today().isoformat()
    today_leaves = [entry for entry in data if today in entry['dates']]
    return render_template('index.html', today_leaves=today_leaves)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', members=TEAM_MEMBERS)

@app.route('/get_leaves')
def get_leaves():
    data = load_data()
    events = []
    for entry in data:
        for leave_date in entry['dates']:
            events.append({
                'title': entry['name'],
                'start': leave_date
            })
    return jsonify(events)

@app.route('/add_leave', methods=['POST'])
def add_leave():
    name = request.form.get('name')
    dates = request.form.getlist('dates[]')
    data = load_data()

    for entry in data:
        if entry['name'] == name:
            entry['dates'] = list(set(entry['dates'] + dates))
            break
    else:
        data.append({'name': name, 'dates': dates})

    save_data(data)
    return jsonify({'status': 'success'})

@app.route('/export_csv')
def export():
    filepath = export_csv(load_data())
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
