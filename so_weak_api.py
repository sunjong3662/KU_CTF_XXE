from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/internal-api', methods=['POST'])
def internal_api():
    xml_data = request.data.decode('utf-8')

    try:
        # XXE 취약점을 만들기 위한 XML 파서 설정
        parser = etree.XMLParser(load_dtd=True, no_network=False)
        doc = etree.fromstring(xml_data, parser=parser)

        # 가정: XML 데이터에는 <file> 태그가 있으며 이는 읽고자 하는 파일의 경로를 포함합니다.
        file_to_read = doc.xpath('//file/text()')[0]

        # 파일을 읽고 내용을 반환합니다.
        with open(file_to_read, 'r') as file:
            data = file.read()

        return data

    except Exception as e:
        return f"An error occurred: {str(e)}", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
