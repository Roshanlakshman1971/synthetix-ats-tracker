"""
Zero-Dependency Local HTTP Server for the Live ATS Tracker Website.
Serves index.html at http://localhost:8080 and exposes /api/download-docx
so DOCX generation works both online and offline.
"""

import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from resume_generator import generate_ats_docx_bytes

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ATSRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/download-docx":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
            docx_bytes = generate_ats_docx_bytes(data)

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            self.send_header("Content-Length", str(len(docx_bytes)))
            self.end_headers()
            self.wfile.write(docx_bytes)
        else:
            self.send_error(404, "Endpoint not found")


if __name__ == "__main__":
    print(f"Starting Live ATS Tracker Website at http://localhost:{PORT}")
    server = HTTPServer(("127.0.0.1", PORT), ATSRequestHandler)
    server.serve_forever()
