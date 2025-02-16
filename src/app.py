from flask import Flask, send_from_directory, request, jsonify
from wss.water_sort_a_star import a_star_solve

app = Flask(__name__, static_folder='../ui/dist', static_url_path='/')


@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/solve', methods=['POST'])
def solve():
    request_data = request.get_json()
    import json

    print(json.dumps(request_data, indent=2))
    solutions = a_star_solve(request_data['tubes'])
    if solutions is None:
        return jsonify({'error': 'No solution found'})

    response = {
        'solution': [{'from': solution.from_tube, 'to': solution.to_tube} for solution in solutions]
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
