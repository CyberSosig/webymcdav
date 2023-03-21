#!/usr/bin/env python3
"""
License: MIT License
"""
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from wsgidav.wsgidav_app import WsgiDAVApp
from wsgidav.fs_dav_provider import FilesystemProvider
import logging

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=80):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    provider = FilesystemProvider("./")
    config = {
        "provider_mapping": {"/": provider},
        "verbose": 1,
        "enable_loggers": [],
    }
    app = WsgiDAVApp(config)
    httpd = server_class(server_address, handler_class)
    httpd.set_app(app)
    logging.info(f"Starting httpd on port {port}...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    run(port=80)
