from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/filereader/status', methods=['GET'])
def filereader_status():
    return jsonify({'status': 'Service is up'})


@app.route('/filereader', methods=['POST'])
def filereader():

    flag_file_path = os.path.join(app.root_path, 'myrealpc')

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
