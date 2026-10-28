import os
import tempfile
from http.server import BaseHTTPRequestHandler

MAX_BYTES = 4 * 1024 * 1024


class handler(BaseHTTPRequestHandler):
    def _send(self, code, body=b"", ctype="text/plain", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > MAX_BYTES:
                return self._send(413, b"File too large for server conversion")
            data = self.rfile.read(length)
            if not data.startswith(b"%PDF"):
                return self._send(400, b"Not a PDF file")

            from pdf2docx import Converter

            with tempfile.TemporaryDirectory() as tmp:
                src = os.path.join(tmp, "in.pdf")
                dst = os.path.join(tmp, "out.docx")
                with open(src, "wb") as f:
                    f.write(data)
                cv = Converter(src)
                try:
                    cv.convert(dst)
                finally:
                    cv.close()
                with open(dst, "rb") as f:
                    out = f.read()
            self._send(
                200,
                out,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except Exception as e:
            self._send(500, ("Conversion failed: %s" % e).encode("utf-8", "ignore")[:300])

    def do_GET(self):
        self._send(200, b"ok")
