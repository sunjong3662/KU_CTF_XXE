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


# 도시 안전도 점검 설정 버튼을 눌렀을 때 safety.html로 이동
@app.route('/connect', methods=['GET', 'POST'])
def safety():
    response_data = "No data received"
    if request.method == 'POST':
        xml_data = request.form['connect_settings']
        # XXE 취약점이 있는지 검사하고, 안전하게 XML을 파싱합니다.
        # 이 예시에서는 의도적으로 XXE 취약점을 허용하는 설정을 사용합니다.
        parser = etree.XMLParser(load_dtd=True, no_network=False, resolve_entities=True)
        try:
            # 받은 XML 데이터를 파싱합니다.
            doc = etree.fromstring(xml_data.encode(), parser=parser)
            # 내부 네트워크 스캐닝을 위해 특정 태그(예: <scanUrl>) 내의 데이터를 사용합니다.
            scan_url = doc.xpath('//scanUrl/text()')
            if scan_url:
                # 내부 또는 외부 자원에 대한 요청을 시뮬레이션합니다.
                # 경고: 실제 환경에서는 외부 요청을 보내는 것이 위험할 수 있습니다.
                response = requests.get(scan_url[0])
                response_data = f"Scanned URL {scan_url[0]}: {response.status_code}, {response.text[:100]}"
            else:
                response_data = "No scan URL found in XML data"
        except Exception as e:
            response_data = f"Error processing XML data: {str(e)}"
    else:
        response_data = "Submit XML data for internal network scanning"

    # 응답 데이터를 safety.html 템플릿에 전달하지 않고, 직접 응답 문자열을 생성하여 반환합니다.
    return make_response(response_data, 200)


@app.route('/energy')
def energy():
    return render_template('energy.html')

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
