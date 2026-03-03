from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import ipinfaux

def create_app():
    app = Flask(__name__)

    @app.errorhandler(HTTPException)
    def handle_error(error):
        return jsonify({
            "success": False,
            "error": {
                "code": error.code,
                "message": error.description
            }
        }), error.code
    
    @app.route("/api/", methods=["GET"])
    def api():
        return jsonify({"success": True})

    @app.route("/api/ip/<string:ip>", methods=["GET"])
    def get_ip(ip):
        jwtToken = ipinfaux.GetJWTByLogin.get_fresh_token()
        data = ipinfaux.GetFullData(ip, jwtToken).as_dict()

        return jsonify({
            "success": True,
            "data": data
        })

    return app

app = create_app()