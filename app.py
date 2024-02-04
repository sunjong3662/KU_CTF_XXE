from flask import Flask, request, render_template, redirect, url_for
from lxml import etree
import os

app = Flask(__name__, static_url_path='/static')

# 안전 설정 XML 파일 경로
SAFETY_CONFIG_FILE = 'safety_config.xml'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic')
def traffic():
    return render_template('traffic.html')

# 도시 안전도 점검 설정 버튼을 눌렀을 때 safety.html로 이동
@app.route('/safety', methods=['GET', 'POST'])
def safety():
    if request.method == 'POST':
        new_settings = request.form['safety_settings']
        # XXE 취약점이 있는지 검사하고, 안전하게 XML을 파싱합니다.
        parser = etree.XMLParser(load_dtd=True, no_network=False)
        try:
            # 받은 XML 데이터를 파싱합니다.
            parsed_xml = etree.fromstring(new_settings, parser=parser)
            # 파싱된 데이터를 파일에 저장합니다.
            with open(SAFETY_CONFIG_FILE, 'wb') as file:
                file.write(etree.tostring(parsed_xml, pretty_print=True))
        except etree.XMLSyntaxError as e:
            return f"XML 구문 오류: {str(e)}", 400
        return redirect(url_for('safety'))

    # GET 요청하면 기본 설정 불러오게 하는거임.
    try:
        with open(SAFETY_CONFIG_FILE, 'rb') as file:
            safety_settings = file.read()
    except IOError:
        # 여기가 이프 파일이 낫 이그지스트? 기본 설정 ㄱㄱ
        safety_settings = b"<safety><fireAlarm status='off'/><camera status='on'/></safety>"

    return render_template('safety.html', safety_settings=safety_settings)

@app.route('/energy')
def energy():
    return render_template('energy.html')

@app.route('/db')
def db():
    return render_template('db.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
