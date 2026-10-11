from flask import Flask, Response, jsonify, request
import requests


SKIPPED_REQUEST_HEADERS = {"host", "user-agent", "content-length", "connection"}
SKIPPED_RESPONSE_HEADERS = {"content-encoding", "content-length", "transfer-encoding", "connection"}
ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=ALLOWED_METHODS)
    def proxy():
        url = request.args.get("url", "")
        if not url.startswith(("http://", "https://")):
            return jsonify(error="Provide a valid http(s) url query parameter"), 400

        headers = {
            key: value
            for key, value in request.headers
            if key.lower() not in SKIPPED_REQUEST_HEADERS
        }
        headers["User-Agent"] = "gzip"

        try:
            upstream = requests.request(
                method=request.method,
                url=f"https://corsproxy.io/?key=e89bea77&url={url}",
                headers=headers,
                data=request.get_data(),
                allow_redirects=False,
                timeout=30,
            )
        except requests.RequestException as error:
            return jsonify(error=str(error)), 502

        response_headers = [
            (key, value)
            for key, value in upstream.headers.items()
            if key.lower() not in SKIPPED_RESPONSE_HEADERS
        ]
        return Response(upstream.content, upstream.status_code, response_headers)

    return app

app = create_app()

