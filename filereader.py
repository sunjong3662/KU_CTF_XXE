from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/filereader/status', methods=['GET'])
def filereader_status():
    return jsonify({'status': 'Service is up'})


@app.route('/filereader', methods=['POST'])
def filereader():
    # 예제에서는 단순히 파일의 내용을 반환하도록 설정합니다.
    # 실제 FLAG 파일의 경로를 지정합니다.
    flag_file_path = os.path.join(app.root_path, 'FLAG')

    try:
        # 파일을 읽고 내용을 반환합니다.
        with open(flag_file_path, 'r') as file:
            flag_content = file.read().strip()
        
        # FLAG 내용을 JSON 형식으로 응답
        return jsonify(flag=flag_content)
    except Exception as e:
        app.logger.error(f"Error reading  file: {e}")
        return "Error processing request", 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7000)
