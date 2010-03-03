#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Reloading WSGI server for development.
# Replacement for 'paster serve --reload pastedeploy.ini'
#
# Waits until the new version of the code loads up before killing the
# running old version. If you save a syntax error you can still use the
# prior version of your application, and it will attempt to reload again
# the next time you save.
#
# Daniel Holth <dholth@fastmail.fm>

import os
import sys
import logging.config
import time
import threading
import ConfigParser
from Queue import Empty

from multiprocessing import Process, Queue, Event
from multiprocessing import active_children
from optparse import OptionParser
from wsgiref.simple_server import make_server

import paste.deploy
import paste.reloader

class Monitor(paste.reloader.Monitor):
    def __init__(self, poll_interval=1, tx=None, rx=None):
        paste.reloader.Monitor.__init__(self, poll_interval)
        self.state = 'RUN'
        self.tx = tx
        self.rx = rx

    def periodic_reload(self):
        while not self.rx.is_set():
            if not self.check_reload():
                self.state = 'STANDBY'
                # inform code change
                self.tx.put({'pid':os.getpid(), 'status':'changed'})
                self.rx.wait(10)
                if self.rx.is_set():
                    return
                self.state = 'RUN'
                self.module_mtimes = {}
            time.sleep(self.poll_interval) 

def serve(server, uri, tx, rx):
    try:
        # configure logging
        config_file = uri
        if config_file.startswith('config:'):
            config_file = config_file.split(':', 1)[1]
        parser = ConfigParser.ConfigParser()
        parser.read([config_file])
        if parser.has_section('loggers'):
            logging.config.fileConfig(config_file)

        # load wsgi application
        app = paste.deploy.loadapp(uri)

        tx.put({'pid':os.getpid(), 'status':'loaded'})

        server.set_app(app)

        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)
        t.start()

        monitor = Monitor(tx=tx, rx=rx)
        monitor.periodic_reload()

    except KeyboardInterrupt:
        pass

def reloadwsgi(uri, host='127.0.0.1', port=8080):
    host = '127.0.0.1'
    port = 8080
    server = make_server(host, port, None)
    
    # tx, rx from the subprocess' perspective.
    tx = Queue()

    def spinup():
        rx = Event()
        worker = Process(target=serve, args=(server, uri, tx, rx))
        worker.rx = rx
        worker.start()
        return worker

    spinup()

    while True:
        try:
            msg = tx.get(True, 1)
            sys.stderr.write("%r\n" % msg)
            if msg['status'] == 'changed':
                spinup()
            elif msg['status'] == 'loaded':
                for worker in active_children():
                    if worker.ident != msg['pid']:
                        worker.rx.set()
        except Empty:
            if not active_children():
                return


def app_factory(global_config, **local_conf):
    import wsgiref.simple_server
    return wsgiref.simple_server.demo_app

if __name__ == "__main__":
    import reloadwsgi
    import pkg_resources
    import os.path
    resource = pkg_resources.resource_filename(__name__, 'test_reloadwsgi.ini')
    resource = os.path.abspath(resource)
    reloadwsgi.reloadwsgi('config:%s' % resource)
