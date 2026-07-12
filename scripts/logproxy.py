#!/usr/bin/env python3
"""
Tiny logging forward-proxy used to capture REAL test traffic.

Sits between a test arm and a SUT: forwards each request to the target port,
returns the SUT's real response, and appends (tag, method, path, status) to a CSV.
Because it records what the JUnit suite ACTUALLY sends at runtime, it captures
dynamic/!concatenated paths (resolveLocation, created-resource ids) that static
source parsing cannot.

Usage:  python logproxy.py <listen_port> <target_port> <logfile> <tag>
Control endpoints (not logged): GET /__ping__  -> 200 ; GET /__shutdown__ -> 200 then exit.
"""
import sys, csv, threading, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LISTEN, TARGET, LOG, TAG = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]

class H(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def _serve(self):
        if self.path in ('/__ping__', '/__shutdown__'):
            self.send_response(200); self.send_header('Content-Length', '0'); self.end_headers()
            if self.path == '/__shutdown__':
                threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        ln = int(self.headers.get('Content-Length', 0) or 0)
        body = self.rfile.read(ln) if ln else None
        hdrs = {k: v for k, v in self.headers.items()
                if k.lower() not in ('host', 'content-length', 'accept-encoding', 'connection')}
        try:
            r = urllib.request.urlopen(
                urllib.request.Request('http://127.0.0.1:%d%s' % (TARGET, self.path),
                                       data=body, method=self.command, headers=hdrs), timeout=20)
            code, data, ct = r.getcode(), r.read(), r.headers.get('Content-Type', 'application/json')
        except urllib.error.HTTPError as e:
            code, data = e.code, (e.read() or b'')
            ct = (e.headers.get('Content-Type') if e.headers else None) or 'application/json'
        except Exception:
            code, data, ct = 599, b'', 'text/plain'
        with open(LOG, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([TAG, self.command, self.path, code])
        self.send_response(code)
        self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(data))); self.end_headers()
        try: self.wfile.write(data)
        except Exception: pass
    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = do_OPTIONS = _serve
    def log_message(self, *a): pass

if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', LISTEN), H).serve_forever()
