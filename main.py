#!/usr/bin/python3
import subprocess
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse
import yaml

CONFIG_PATH = "/etc/webview-server/config.yml"
KIOSK_PATH = "/usr/local/bin/kiosk"
WWW_PATH = "/var/webview-server/www/"
DB_PATH = "/etc/webview-server"


app = Flask("wv-server", template_folder='web/')
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
        if request.form['action'] == 'open':
            url = request.form['url']
            if url != "":
                new_History = History(url=url)
                db.session.add(new_History)
                db.session.commit()
                kill_children_pids()
                start_webview(check_and_add_protocol(url))
        elif request.form['action'] == 'close':
            kill_children_pids()
        elif request.form['action'] == 'reopen':
            last_record = History.query.order_by(History.id.desc()).first().url
            print(last_record)
            kill_children_pids()
            start_webview(check_and_add_protocol(last_record))
            
        elif request.form['action'] == 'favorite':
            url = request.form['url']
            if Favorite.query.filter_by(url=url).first() == None:
                new_Favorite = Favorite(url=url)
                db.session.add(new_Favorite)
                db.session.commit()
        elif request.form['action'] == 'del':
            url = request.form['url']
            rm_Favorite = Favorite.query.filter_by(url=url).first()
            db.session.delete(rm_Favorite)
            db.session.commit()

    favorites = Favorite.query.order_by(Favorite.id.desc()).all()
    histories = History.query.order_by(History.id.desc()).limit(10).all()
    return render_template('index.html', histories=histories, favorites=favorites )

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

if __name__ == '__main__':
    http_port,http_address = parse_config()
    app.run(host=http_address, port=http_port, debug=False)
