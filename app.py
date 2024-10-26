from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return "Hello World"

@app.route("/about", methods=['GET'])
def about():
    return make_response(jsonify({"nama": "Alfian", "umur": "20"}))

if __name__ == "__main__" :
    app.run()