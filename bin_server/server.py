#!/usr/bin/env python

from time import sleep
import threading
from SocketServer import ThreadingTCPServer, StreamRequestHandler


class ThreadingServer(ThreadingTCPServer):
    allow_reuse_address = 1


class RequestHandler(StreamRequestHandler):
    def handle(self):
        print 'Connected with %s' % str(self.client_address[0])
        a = self.rfile.readline().strip()
        print 'Got text "%s"' % a
        sleep(10)
        self.wfile.write('You wrote: %s' % a.upper())
        print 'End request from %s' % str(self.client_address[0])


if __name__ == '__main__':
    address = ('', 50000)
    server = ThreadingServer(address, RequestHandler)
    server.serve_forever()

