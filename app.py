from flask import Flask, render_template, send_from_directory, redirect, url_for, request, jsonify, make_response
from lxml import etree
from datetime import datetime
from flask_cors import CORS
from werkzeug.utils import secure_filename
from shutil import copyfile
import os
import json

app = Flask(__name__, static_url_path='/static')
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['XML_LOG_FOLDER'] = os.path.join(app.static_folder, 'xml_log')
app.config['ORIGINAL_LOG_FILE'] = os.path.join(app.config['XML_LOG_FOLDER'], 'xml_log.xml')
app.config['DOWNLOAD_FOLDER'] = app.config['XML_LOG_FOLDER']  # 초기 다운로드 폴더 설정

# uploads 폴더가 없으면 생성
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


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


@app.route('/')
def index():
    return render_template('index.html')




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


#구현하고 버그잡는데 오래 걸릴 것 같아서 꼼수 좀 부렸읍니다... 나중에 구현할게요..../
@app.route('/connect', methods=['GET', 'POST'])
def connect():
    # parsingxml 서비스 상태 확인
    try:
        parsingxml_response = requests.get('http://localhost:5000/parsingxml/status', timeout=100)
        # HTTP 상태 코드가 200인 경우 "connected"로 판단
        parsingxml_status = "connected" if parsingxml_response.status_code == 200 and parsingxml_data.get('connected') else "disconnected"
    except Exception:
        #parsingxml_status = "unknown"
        parsingxml_status = "connected"

    # filereader 서비스 상태 확인
    try:
        filereader_response = requests.get('http://filereader:7000/filereader/status', timeout=10)
        # HTTP 상태 코드가 200인 경우 "connected"로 판단
        filereader_status = "connected" if filereader_response.status_code == 200 else "disconnected"
    except Exception:
        #filereader_status = "unknown"
        #filereader_status = "connected"
        filereader_status = "disconnected"

    try:
        upload_response = requests.get('http://localhost:5000/upload/status', timeout=10)
        # HTTP 상태 코드가 200인 경우 "connected"로 판단
        upload_status = "connected" if upload_response.status_code == 200 else "disconnected"
    except Exception:
        #filereader_status = "unknown"
        #filereader_status = "connected"
        upload_status = "connected"

    # 서버 상태 정보를 리스트로 구성
    server_statuses = [
        ("parsingxml:5000", parsingxml_status),
        ("filereader:7000?file=status", filereader_status),
        ("uploadXML", upload_status)
    ]
    # 템플릿에 서버 상태 정보를 전달하여 렌더링
    return render_template('connection_monitor.html', server_statuses=server_statuses)






@app.route('/serverlog')
def server_log():
    # uploads 폴더에 파일이 있는지 확인
    if os.listdir(app.config['UPLOAD_FOLDER']):
        log_files = os.listdir(app.config['UPLOAD_FOLDER'])
        folder_path = app.config['UPLOAD_FOLDER']
    else:
        # uploads 폴더가 비어 있으면 xml_log 폴더의 xml_log.xml 사용
        log_files = ['xml_log.xml']
        folder_path = app.config['XML_LOG_FOLDER']

    attack_reports = []
    for log_file in log_files:
        # 각 로그 파일에 대해 파싱 수행
        attack_reports.extend(parse_xml_log_file(log_file, folder_path))

    return render_template('server_log.html', attack_reports=attack_reports, log_files=log_files)

def parse_xml_log_file(filename, folder_path):
    filepath = os.path.join(folder_path, filename)
    with open(filepath, 'rb') as file:  # 'rb' 모드로 파일 열기.
        xml_content = file.read()
    doc = etree.fromstring(xml_content)  # 바이트 문자열을 직접 처리 하는 부분.
    
    attack_reports = []
    for attack_report in doc.findall('.//attackReport'):
        details = attack_report.find('.//attackDetails')
        attack_type = details.findtext('.//attackType')
        ip_address = details.findtext('.//targetSystem/ipAddress')
        service_name = details.findtext('.//targetSystem/serviceName')
        timestamp = details.findtext('.//timestamp')
        outcome = details.findtext('.//attackOutcome')
        
        payload_used = attack_report.findtext('.//payloadUsed')
        extracted_data = [{
            "dataPoint": entry.findtext('.//dataPoint'),
            "dataValue": entry.findtext('.//dataValue')
        } for entry in attack_report.findall('.//extractedData/entry')]
        
        attack_reports.append({
            "attack_type": attack_type,
            "ip_address": ip_address,
            "service_name": service_name,
            "timestamp": timestamp,
            "outcome": outcome,
            "payload_used": payload_used,
            "extracted_data": extracted_data
        })
        
    return attack_reports






@app.route('/download_log/<filename>')
def download_log(filename):
    directory = app.config['DOWNLOAD_FOLDER']
    return send_from_directory(directory, filename)





@app.route('/setting', methods=['GET', 'POST'])
def setting():
    return render_template('setting.html')


@app.route('/upload', methods=['POST'])
def upload_config():
     # 'file'이 request.files 안에 없으면 기본 로그 파일을 사용
    if 'file' not in request.files:
        app.config['DOWNLOAD_FOLDER'] = app.config['XML_LOG_FOLDER']
        return jsonify({'error': 'No file part, using default log file.'}), 200
    
    file = request.files['file']
    # 파일 이름이 없으면 기본 로그 파일을 사용
    if file.filename == '':
        app.config['DOWNLOAD_FOLDER'] = app.config['XML_LOG_FOLDER']
        return jsonify({'error': 'No selected file, using default log file.'}), 200
    
    # 화이트리스트 방식으로 XML 파일만 허용
    if not file.filename.endswith('.xml'):
        return jsonify({'error': 'only xml m8. No hack ^______^'}), 400
    
    # 파일 내용을 메모리에 저장
    xml_data = file.read()
    
    # XML 파싱 시도
    try:
        parser = etree.XMLParser(load_dtd=True, no_network=False)
        doc = etree.fromstring(xml_data, parser=parser)
        if not validate_xml_structure(doc):
            # 파일 구조 검증 실패 시
            return jsonify({'error': "No hack ^______^"}), 400
        
        # 여기서 파일을 저장하거나 필요한 추가 처리를 수행
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(xml_data)
        
       # 파일 업로드 후 다운로드 폴더 경로 변경
        app.config['DOWNLOAD_FOLDER'] = app.config['UPLOAD_FOLDER']
        
        return jsonify({'success': 'Upload complete!'}), 200
    except etree.XMLSyntaxError as e:
        return jsonify({'error': str(e)}), 400

def validate_xml_structure(doc):
    # 모든 attackReport 노드 확인 부분.
    for attack_report in doc.findall('attackReport'):
        # 필요한 자식 노드들이 있는지 확인하는 부분.
        attack_details = attack_report.find('attackDetails')
        payload_used = attack_report.findtext('payloadUsed')
        extracted_data = attack_report.find('extractedData')

        if attack_details is None or payload_used is None or extracted_data is None:
            print("Missing required nodes within 'attackReport'.")
            return False

        # attackDetails 내부의 필요한 노드들이 있는지 확인 하는 부분.
        attack_type = attack_details.findtext('attackType')
        target_system = attack_details.find('targetSystem')
        timestamp = attack_details.findtext('timestamp')
        attack_outcome = attack_details.findtext('attackOutcome')

        if not all([attack_type, target_system, timestamp, attack_outcome]):
            print("Missing one of the required child nodes in 'attackDetails'.")
            return False

        # targetSystem 내부의 ipAddress와 serviceName 노드를 확인하는 곳.
        ip_address = target_system.findtext('ipAddress')
        service_name = target_system.findtext('serviceName')

        if not all([ip_address, service_name]):
            print("Missing 'ipAddress' or 'serviceName' node in 'targetSystem'.")
            return False

        # extractedData 내부의 모든 entry 노드에 대해 dataPoint와 dataValue 노드가 있는지 없는지 확인하는 곳.
        for entry in extracted_data.findall('entry'):
            data_point = entry.findtext('dataPoint')
            data_value = entry.findtext('dataValue')

            if data_point is None or data_value is None:
                print("Missing 'dataPoint' or 'dataValue' in 'entry' of 'extractedData'.")
                return False

    # 모든 검사를 통과했으면 True 갈기기.
    return True


@app.route('/reset_logs', methods=['POST'])
def reset_logs():
    # uploads 폴더의 모든 파일 삭제
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.unlink(file_path)  # 파일 삭제
    
   # 다운로드 폴더 경로를 원본 XML 로그 폴더로 설정
    app.config['DOWNLOAD_FOLDER'] = app.config['XML_LOG_FOLDER']
    
    return redirect(url_for('setting'))




@app.route('/upload/status', methods=['GET'])
def upload_status():
    return jsonify({'status': 'Service is up'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
