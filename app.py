from flask import Flask, request, render_template, redirect, url_for
from lxml import etree
import os

app = Flask(__name__, static_url_path='/static')

# 안전 설정 XML 파일 경로
SAFETY_CONFIG_FILE = 'safety_config.xml'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic', methods=['GET', 'POST'])
def traffic():
    video_src = "/static/videos/default.mp4"  # 기본 비디오 소스
    if request.method == 'POST':
        xml_data = request.form['xml_data']
        try:
            # XXE 취약점을 트리거할 수 있는 파서 설정
            parser = etree.XMLParser(load_dtd=True, no_network=False, resolve_entities=True)
            doc = etree.fromstring(xml_data.encode(), parser=parser)
            # 입력받은 위치에 해당하는 영상 URL 추출
            video_src = doc.find('.//video').text
        except Exception as e:
            print(f"Error: {e}")
    return render_template('traffic.html', video_src=video_src)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    server_statuses = []
    if request.method == 'POST':
        xml_data = request.form['connect_settings']
        # XXE 취약점을 이용하여 파싱 설정
        parser = etree.XMLParser(load_dtd=True, no_network=False, resolve_entities=True)
        try:
            doc = etree.fromstring(xml_data.encode(), parser=parser)
            # <server> 태그 내의 각 서버 정보를 파싱
            for server in doc.findall('.//server'):
                server_name = server.find('name').text
                server_url = server.find('url').text
                try:
                    # 각 서버 URL에 대한 상태 체크를 시뮬레이션
                    response = requests.get(server_url, timeout=5)
                    status = "Connected" if response.status_code == 200 else "Disconnected"
                except Exception:
                    status = "Disconnected"
                server_statuses.append((server_name, status))
        except Exception as e:
            return f"Error processing XML data: {str(e)}", 400
    else:
        # POST 요청이 아닌 경우, 빈 상태 정보를 전달
        server_statuses = [("Server A", "Unknown"), ("Server B", "Unknown"), ("Server C", "Unknown")]

    # connection_monitor.html 템플릿으로 상태 정보를 전달
    return render_template('connection_monitor.html', server_statuses=server_statuses)


@app.route('/safety')
def energy():
    return render_template('safety.html')

@app.route('/db', methods=['GET', 'POST'])
def db():
    if request.method == 'POST':
        xml_data = request.form['xml_data']
        # XXE 취약점이 있는지 검사하고, XML을 파싱합니다.
        parser = etree.XMLParser(load_dtd=True, no_network=False)
        try:
            # 받은 XML 데이터를 파싱합니다.
            parsed_xml = etree.fromstring(xml_data, parser=parser)
            # 파싱된 데이터를 파일에 저장합니다.
            with open(SAFETY_CONFIG_FILE, 'wb') as file:
                file.write(etree.tostring(parsed_xml, pretty_print=True))
            # 성공 메시지를 반환합니다.
            return 'XML 데이터가 성공적으로 업데이트 되었습니다.'
        except etree.XMLSyntaxError as e:
            return f"XML 구문 오류: {str(e)}", 400
        except Exception as e:
            return f"처리 중 오류 발생: {str(e)}", 500

    # GET 요청 시 DB 페이지를 렌더링합니다.
    return render_template('db.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
