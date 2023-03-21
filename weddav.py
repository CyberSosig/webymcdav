#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers

Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from wsgidav.wsgidav_app import WsgiDAVApp
from cheroot.wsgi import Server as WSGIServer
from cheroot.wsgi import PathInfoDispatcher
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('0.0.0.0', port)

    # Configure WebDAV
    config = {
        "host": "0.0.0.0",
        "port": port,
        "provider_mapping": {"/webdav": "."},
        "dir_browser": {"enable": True},
    }
    wsgi_dav_app = WsgiDAVApp(config)

    # Setup WSGI server with HTTP and WebDAV handlers
    dispatcher = PathInfoDispatcher({'/': handler_class, '/webdav': wsgi_dav_app})
    httpd = WSGIServer(server_address, dispatcher)

    logging.info('Starting httpd...\n')
    try:
        httpd.start()
    except KeyboardInterrupt:
        pass
    httpd.stop()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
