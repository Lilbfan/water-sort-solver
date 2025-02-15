from flask import Flask, send_from_directory
from flask import request

app = Flask(__name__, static_folder='../ui/dist', static_url_path='/')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/solve', methods=['POST'])
def solve():
    request_data = request.get_json()
    print(request_data)
    response = {
        "solution": "This is the solution"
    }
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

