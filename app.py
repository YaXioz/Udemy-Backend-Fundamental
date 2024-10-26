from flask import Flask, request, jsonify
import mysql.connector
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "baw87ftfw8f23f32wf2h98qeqd21jdil"

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.header.get("JWT")
        if not token:
            return jsonify({"data": "Token Required", "code": 403}), 403
        
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"data":"Token Invalid", "code": 403}), 403
        return f(*args, **kwargs)
    return decorator

mydb = mysql.connector.connect (
    host="localhost",
    user="root",
    password="",
    database="liveapp"
)

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if(data['username'] == "admin" and data['password'] == "admin123"):
            token = jwt.encode({"user": data['username'], "exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config["SECRET_KEY"])
            return jsonify({"data": token.decode("UTF-8"), "code": 200}), 200
        else:
            return jsonify({"data":"Login was Invalid", "code": 403}), 403
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500
    
@app.route("/barang", methods=['GET'])
@token_required
def getBarang():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM barang")
        result = []
        for i in cursor.fetchall():
            result.append({
                "id": i[0],
                "nama": i[1],
                "harga": i[2]
            })
        return jsonify({"data":result, "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/barang/<int:id>", methods=['GET'])
@token_required
def getBarangbyID(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM barang WHERE id = %s" % (id))
        data = cursor.fetchone()
        result = {
            "id": data[0],
            "nama": data[1],
            "harga": data[2]
        }
        return jsonify({"data": result, "code":200}), 200
    except Exception as e:
        return jsonify({"data": str(e), "code": 500}), 500

@app.route("/barang", methods=['POST'])
@token_required
def insertBarang():
    try:
        data = request.json
        cursor = mydb.cursor()
        sql = "INSERT INTO barang (id, nama, harga) VALUES (NULL, %s, %s)"
        value = (data['nama'], data['harga'])
        cursor.execute(sql, value)
        mydb.commit()
        return jsonify({"data":"1 Record Inserted!", "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/barang/<int:id>", methods=['PUT'])
@token_required
def updateBarangbyID(id):
    try:
        data = request.json
        cursor = mydb.cursor()
        sql = "UPDATE barang SET nama = %s, harga = %s WHERE id = %s"
        value = (data['nama'], data['harga'], id)
        cursor.execute(sql, value)
        mydb.commit()
        return jsonify({"data":"1 Record Affected!", "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

@app.route("/barang/<int:id>", methods=['DELETE'])
@token_required
def deleteBarangbyID(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM barang WHERE id = %s" % (id,))
        return jsonify({"data": "1 Record Deleted!", "code": 200}), 200
    except Exception as e:
        return jsonify({"data":str(e), "code": 500}), 500

if "__main__" == __name__:
    app.run(debug=True, host="0.0.0.0", port=1000)
