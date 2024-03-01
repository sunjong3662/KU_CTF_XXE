from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/filereader/status', methods=['GET'])
def filereader_status():
    return jsonify({'status': 'Service is up'})

# 'GET' 메소드를 허용하고, 'file' 파라미터를 통해 파일 이름을 받습니다.
@app.route('/filereader', methods=['GET'])
def filereader():
    # 'file' 파라미터를 사용하여 경로를 구성합니다.
    file_name = request.args.get('file', '')
    file_path = os.path.join(app.root_path, file_name)

    try:
        # 파일을 열고 내용을 읽습니다.
        with open(file_path, 'r') as file:
            content = file.read().strip()
        # 파일 내용을 JSON 형식으로 응답합니다.
        return jsonify(content=content)
    except Exception as e:
        app.logger.error(f"Error reading file: {e}")
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
