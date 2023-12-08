from flask import Flask, redirect, url_for, request, Response, jsonify
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world"


@app.errorhandler(404)
def notFound(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route("/titles", methods=['GET'])
def tytuly():
    if request.method == 'GET':
        with open('animations.json') as jsonData:
            result = []
            data = json.load(jsonData)
            for animation in data['animations']:
                result.append(animation['Original title'])
            js = json.dumps(result)
            resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/ids/<id>", methods=['GET'])
def ids(id):
    if (int(id) <= 5):
        with open('animations.json') as jsonData:
            data = json.load(jsonData)
            for animation in data['animations']:
                if id == str(animation['ID']):
                    js = json.dumps(animation)
        resp = Response(js, status=200, mimetype='application/json')
    else:
        message = {
            'status': 404,
            'message': 'Nie ma takiego ID!'
        }
        resp = jsonify(message)
        resp.status_code = 404
    return resp


@app.route("/titles/<keyword>", methods=['GET'])
def titlesKeyword(keyword):
    with open('animations.json') as jsonData:
        result = []
        data = json.load(jsonData)
        for animation in data['animations']:
            if (keyword in animation['Keywords']):
                result.append(animation['Original title'])
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/studios/<id>", methods=["GET","PUT"])
def studiosChange(id):
    if request.method == "GET":
        with open('animations.json') as jsonData:
            result = []
            data = json.load(jsonData)
            for animation in data['animations']:
                if id == str(animation['ID']):
                    result.append(animation['Studio'])
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    elif request.method == "PUT":
        studio = request.args.get("studio")
        with open('animations.json') as jsonData:
            result = []
            data = json.load(jsonData)
            for animation in data['animations']:
                if id == str(animation['ID']):
                    animation["Studio"] = studio
                    result.append(animation)
        js = json.dumps(result)
        resp = Response(js, status=200, mimetype='application/json')
        message2 = {
            'status': 200,
            'message': f'Studio changed successfully for: {studio}'
        }
        resp2 = jsonify(message2)
    return resp2
