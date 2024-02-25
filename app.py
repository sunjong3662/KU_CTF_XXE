from flask import Flask, jsonify, make_response, request, render_template, redirect, url_for
from lxml import etree
from datetime import datetime
import os
import json

app = Flask(__name__, static_url_path='/static')

# 안전 설정 XML 파일 경로
SAFETY_CONFIG_FILE = 'safety_config.xml'

@app.route('/')
def index():
    return render_template('index.html')


congestion_data = {
    "철산대교": "원활"
}

# 도로 이름과 비디오 경로의 매핑
road_video_mapping = {
    "철산대교": "/static/videos/chulsandaegyo.mp4",
}



# 도로 이름과 비디오 경로의 매핑
road_video_mapping = {
    "용산 한강": "/static/videos/yongsanhangang.mp4",
    "강남대치동": "/static/videos/gangnamdaechi.mp4",
    "강남대로": "/static/videos/gangnamdaero.mp4",
    "가양대교북쪽": "/static/videos/gayangdaegyonorth.mp4",
    "가양IC": "/static/videos/gayangIC.mp4",
    "화양사거리": "/static/videos/hwayangsagori.mp4",
    "진암": "/static/videos/jinam.mp4",
    "철산대교": "/static/videos/chulsandaegyo.mp4",
    # 다른 도로 이름과 비디오 경로 매핑 추가
}



@app.route('/parsingxml', methods=['POST'])
def parse_xml():
    xml_data = request.data
    try:
        # XML 파서 설정: DTD 로드, 엔티티 해석 활성화
        parser = etree.XMLParser(load_dtd=True, no_network=False, resolve_entities=True)
        doc = etree.fromstring(xml_data, parser=parser)
        
        # roadId 값 추출
        road_id = doc.find('.//roadId').text
        
        # trafficData.xml 파일에서 해당 roadId에 맞는 videoPath와 congestion 값 추출
        xml_file_path = os.path.join(app.root_path, 'static', 'xml', 'trafficData.xml')
        with open(xml_file_path, 'rb') as xml_file:
            xml_content = xml_file.read()
            traffic_doc = etree.fromstring(xml_content)
            road_element = traffic_doc.xpath(f"//road[@id='{road_id}']")
            if road_element:
                video_path = road_element[0].find('videoPath').text
                congestion = road_element[0].find('congestion').text
                response_xml = f'<response><videoSrc>{video_path}</videoSrc><congestion>{congestion}</congestion></response>'
                return make_response(response_xml, 200, {'Content-Type': 'application/xml'})
            else:
                return make_response('<error>Information not found</error>', 404, {'Content-Type': 'application/xml'})
    except Exception as e:
        app.logger.error(f"Error processing XML data: {e}")
        return make_response(f'<error>Error processing XML data: {str(e)}</error>', 400, {'Content-Type': 'application/xml'})


@app.route('/parsingxml/status', methods=['GET'])
def parsingxml_status():
    return jsonify({'status': 'Service is up'})


@app.route('/traffic')
def traffic():
    return render_template('traffic.html')




@app.route('/connect', methods=['GET', 'POST'])
def connect():
    try:
        parsingxml_response = requests.get('http://ctf.bulletproofyuri.kr:2024/parsingxml/status', timeout=10)
        # 응답 문자열이 정확히 일치하는지 확인
        parsingxml_status = "connected" if parsingxml_response.text == "{'status': 'Service is up'}" else "disconnected"
    except Exception:
        parsingxml_status = "disconnected"

    try:
        filereader_response = requests.get('http://127.0.0.1:7000/filereader/status', timeout=10)
        # 응답 문자열이 정확히 일치하는지 확인
        filereader_status = "connected" if filereader_response.text == "{'status': 'Service is up'}" else "disconnected"
    except Exception:
        filereader_status = "disconnected"

    server_statuses = [
        ("parsingxml:5000", parsingxml_status),
        ("filereader:7000?file=status", filereader_status),
        ("숨겨진 네트워크", "unknown")
    ]
    return render_template('connection_monitor.html', server_statuses=server_statuses)






@app.route('/safety')
def safety():
    #미정
    return render_template('safety.html')






@app.route('/db', methods=['GET', 'POST'])
def db():
    #미정
    return render_template('db.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
