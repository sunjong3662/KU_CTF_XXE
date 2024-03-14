from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/filereader/status', methods=['GET'])
def filereader_status():
    return jsonify({'status': 'Service is up'})

@app.route('/filereader', methods=['GET'])
def filereader():
    file_name = request.args.get('file', '')
    file_path = os.path.join(app.root_path, file_name)

    try:
       with open(file_path, 'r') as file:
            content = file.read().strip()
            return jsonify(content=content)
    except Exception as e:
        app.logger.error(f"Error reading file: {e}")
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
