from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route("/", methods=['GET'])
def root():
    return "Hello World"