"""Basic functions to create response."""

from flask import jsonify


class FactoryResponse(object):
    """Factory class for response messages."""

    def new201(self, data):
        """Response 201 message."""
        resp = jsonify(data)
        resp.content_type = "application/json"
        resp.status_code = 201
        return resp

    def new202(self):
        """Response 202 message."""
        resp = jsonify()
        resp.content_type = "application/json"
        resp.status_code = 202
        return resp

    def new200(self, data=None):
        """Response 200 message, on successfull call."""
        resp = jsonify(data)
        resp.content_type = "application/json"
        resp.status_code = 200
        return resp

    def new400(self):
        """Response 400 message, otherwhise."""
        resp = jsonify()
        resp.content_type = "application/json"
        resp.status_code = 400
        return resp

    def new401(self):
        """Response 401 message, on unauthorized call."""
        resp = jsonify()
        resp.content_type = "application/json"
        resp.status_code = 401
        return resp

    def new404(self, data=None):
        """Response 404 message, on unauthorized call."""
        resp = jsonify(data)
        resp.content_type = "application/json"
        resp.status_code = 404
        return resp

    def new429(self):
        """Response 404 message, on unauthorized call. When rate limit is hit."""
        resp = jsonify()
        resp.content_type = "application/json"
        resp.status_code = 429
        return resp

    def new405(self):
        """Response 405 message, on unauthorized call. not defined methods."""
        resp = jsonify()
        resp.content_type = "application/json"
        resp.status_code = 404
        return resp
