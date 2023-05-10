from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Teste de Deploy": "Welcome to your Flask app 🚅"})


@app.route('/rota')
def index():
    return jsonify({"Teste de Deploy": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
