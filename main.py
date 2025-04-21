#!/usr/bin/python3
"""Main server script for Flask web interface."""
import os
import urllib.parse
import subprocess
import yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

CONFIG_PATH = "/etc/webview-server/config.yml"
KIOSK_PATH = "/usr/local/bin/kiosk"
WWW_PATH = "/webview-server/www/"
DB_PATH = "/webview-server"

app = Flask("wv-server", template_folder=WWW_PATH)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}/data.db'
db = SQLAlchemy(app)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form['action']
        raw_input = request.form.get('url', '').strip()

        if action == 'open' and raw_input:
            urls = [check_and_add_protocol(u.strip()) for part in raw_input.splitlines() for u in part.split(',') if u.strip()]
            if urls:
                db.session.add(History(url=raw_input))
                db.session.commit()
                kill_children_pids()
                start_webview_multiple(urls)

        elif action == 'close':
            kill_children_pids()

        elif action == 'reopen':
            last_record = History.query.order_by(History.id.desc()).first()
            if last_record:
                kill_children_pids()
                start_webview_multiple([check_and_add_protocol(last_record.url)])

        elif action == 'favorite':
            if raw_input and not Favorite.query.filter_by(url=raw_input).first():
                db.session.add(Favorite(url=raw_input))
                db.session.commit()

        elif action == 'del':
            rm_Favorite = Favorite.query.filter_by(url=raw_input).first()
            if rm_Favorite:
                db.session.delete(rm_Favorite)
                db.session.commit()

    favorites = Favorite.query.order_by(Favorite.id.desc()).all()
    histories = History.query.order_by(History.id.desc()).limit(10).all()
    return render_template('index.html', histories=histories, favorites=favorites)


def start_webview(link):
    try:
        print("Open WebView: "+ link)
        p = subprocess.Popen(["python3",KIOSK_PATH, "--urls"] + link, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def parse_config():

    try:
        with open(CONFIG_PATH, 'r') as file:
            config = yaml.safe_load(file)
        http_port = config["network"]['port']
        http_address = config["network"]['listen_ip']
    except: 
        print("Config error, set default vars")
        http_port = 80
        http_address = "0.0.0.0"

    return http_port,http_address

def start_webview_multiple(urls):
    try:
        args = ["python3", KIOSK_PATH, "--urls"] + urls
        print(f"Open multiple WebViews: {urls}")
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f'Error opening multiple WebViews: {e}')

if __name__ == '__main__':
    http_port,http_address = parse_config()
    app.run(host=http_address, port=http_port, debug=False)
