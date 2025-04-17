from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'data.json'

members = [
    "v-asasane", "v-ayushg", "v-aysaini", "v-bhagpatil", "v-ckendre", "v-chevukumar",
    "v-chintreddy", "v-dvengala", "v-dgadave", "v-gdiwakar", "v-krutwik", "v-kotasatya",
    "v-krshinde", "v-mgire", "v-nrenuka", "v-nisbhavsar", "v-deshmukhp", "v-pthengane",
    "v-yadavprade", "v-ragaikwad", "v-rashmsingh", "v-saurabhv", "v-snambissan",
    "v-shwetabais", "v-sshelke", "v-trunwal", "v-ubhuvibhar"
]

@app.route('/')
def index():
    try:
        with open(DATA_FILE, 'r') as f:
            records = json.load(f)
        today_str = datetime.today().strftime('%Y-%m-%d')
        today_leaves = [r for r in records if r["date"] == today_str]
    except:
        today_leaves = []
    return render_template('index.html', today_leaves=today_leaves)

@app.route('/calendar')
def calendar_view():
    return render_template('calendar.html', members=members)

@app.route('/add_leave', methods=['POST'])
def add_leave():
    name = request.form.get('name')
    dates = request.form.getlist('dates[]')

    try:
        with open(DATA_FILE, 'r+') as f:
            existing = json.load(f)
            for date in dates:
                existing.append({"name": name, "date": date})
            f.seek(0)
            json.dump(existing, f, indent=2)
            f.truncate()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_leaves')
def get_leaves():
    try:
        with open(DATA_FILE, 'r') as f:
            records = json.load(f)
        events = [{"title": r["name"], "start": r["date"]} for r in records]
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_leave', methods=['POST'])
def delete_leave():
    data = request.get_json()
    name = data.get("name")
    date = data.get("date")

    if not name or not date:
        return jsonify({"error": "Missing name or date"}), 400

    try:
        with open(DATA_FILE, 'r+') as f:
            records = json.load(f)
            updated = [r for r in records if not (r["name"] == name and r["date"] == date)]
            f.seek(0)
            json.dump(updated, f, indent=2)
            f.truncate()
        return jsonify({"status": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
