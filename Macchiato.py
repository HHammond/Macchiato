
import logging
import tornado.auth
import tornado.escape

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import os.path
import argparse

import sqlite3
import json

import Macchiato.models as models
import Macchiato.datastore

import utils.filescanner

NOTEBOOK_STORE = "./storage"

class CommentHandler(tornado.web.RequestHandler):
	def get(self, comment_id=None):
		if comment_id:
			self.write("Requested comment " + comment_id)
		else: 
			self.write('dickbutt')

class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

application = tornado.web.Application([
	(r"/notebook/(.*\.html)", MyStaticFileHandler, {'path': './notebooks'}),
	(r"/cs/cell_([0-9]+)", CommentHandler),

	(r'/static/(.*)', MyStaticFileHandler, {'path': './static'}),
])

def init_app():
	# initialize models
	Macchiato.datastore.create_tables()

def run():
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8081)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	
	# get notebook folder
	global NOTEBOOK_DIR
	parser = argparse.ArgumentParser()
	parser.add_argument("f", help="Notebook folder")
	args = parser.parse_args()
	NOTEBOOK_DIR = args.f
	
	init_app()
	run()
