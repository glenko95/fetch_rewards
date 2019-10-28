from flask import Flask
from flask import request, jsonify
from collections import Counter

app = Flask(__name__)

class BadRequest(Exception):
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    # catch BadRequest exception globally, serialize to JSON and return status code 400--invalid data
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400


@app.route('/api/v1/resources/pyramid_word', methods=['POST'])
def pyramid_word():
    _word = request.get_json()["word"]
    if type(_word) is not str:
        raise BadRequest('Invalid data type', 400, {"received_data_type": type(_word).__name__, "valid_data_type": 'str'})

    if len(_word) == 0:
        return jsonify({'result': False}), 200
    char_freq = list(Counter(_word).values())
    char_freq.sort()
    for i in range(len(char_freq)):
        # verifying that the array is strictly ascending is O(n)
        if char_freq[i] != i + 1:
            return jsonify({'result': False}), 200
    return jsonify({'result': True}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
