from flask import jsonify, json
#TODO add unit tests for this class
class FactoryResponse(object):
    def new201(self,data):
        resp = jsonify(data)
        resp.content_type="application/json"
        resp.status_code=201
        return resp

    def new202(self):
        resp = jsonify()
        resp.content_type="application/json"
        resp.status_code=202
        return resp

    def new200(self):
        resp = jsonify()
        resp.content_type="application/json"
        resp.status_code=200
        return resp
    def new400(self):
        resp = jsonify()
        resp.content_type="application/json"
        resp.status_code=400
        return resp
    def new403(self):
        resp = jsonify()
        resp.content_type="application/json"
        resp.status_code=403
        return resp
