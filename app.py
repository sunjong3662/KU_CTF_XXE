from flask import Flask, request, render_template
import requests
from lxml import etree


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/traffic')
def traffic():
    return render_template('traffic.html')

# 도시 안전도 점검 설정 버튼을 눌렀을 때 safety.html로 이동
@app.route('/safety')
def safety():
    return render_template('safety.html')

# 에너지 관리 설정 버튼을 눌렀을 때 energy.html로 이동
@app.route('/energy')
def energy():
    return render_template('energy.html')

# DB 관리 버튼을 눌렀을 때 db.html로 이동
@app.route('/db')
def db():
    return render_template('db.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
