#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

import sockjs.tornado

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class MainHandler(sockjs.tornado.SockJSConnection):
    @tornado.gen.coroutine
    def outer(self):
        logging.info('outer starts')
        yield self.inner()
        yield self.inner()  
        logging.info('outer ends')  
        raise tornado.gen.Return('hello')

    @tornado.gen.coroutine
    def inner(self):
        logging.info('inner runs')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def open(self):
        res = yield self.outer()
        self.write(res)

if __name__ == "__main__":
    tornado.options.parse_command_line()

    MainRouter = sockjs.tornado.SockJSRouter(MainHandler, '/test')


    app = tornado.web.Application(list(MainRouter.urls))

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
