#!/usr/bin/python3
import subprocess
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse


KIOSK_PATH = "./kiosk.py"

app = Flask(__name__, template_folder='web/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action'] == 'open':
            url = request.form['url']
            if url != "":
                new_entry = Entry(url=url)
                db.session.add(new_entry)
                db.session.commit()
                kill_children_pids()
                start_webview(check_and_add_protocol(url))
        elif request.form['action'] == 'close':
            kill_children_pids()
        elif request.form['action'] == 'reopen':
            kill_children_pids()
            last_record = Entry.query.order_by(Entry.id.desc()).first()
            start_webview(check_and_add_protocol(last_record))

    entries = Entry.query.order_by(Entry.id.desc()).limit(10).all()
    return render_template('index.html', entries=entries)


def start_webview(link):
    try:
        print("Open WebView: "+ link)
        p = subprocess.Popen(["python3",KIOSK_PATH, "--url", link], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f'Error opening WebView: {e}')

def kill_children_pids():
    pid = os.getpid()
    os.system("kill $(pgrep -P "+str(pid)+")")

def check_and_add_protocol(url):
    url = urllib.parse.unquote(url)
    # print('check_and_add_protocol', url)
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
