
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

NOTEBOOK_DIR = None
application = None

base = os.path.dirname(os.path.realpath(__file__))
class CommentHandler(tornado.web.RequestHandler):
	def get(self, **kwargs):

		# Create notebook object if not exists
		try:
			notebook = models.Notebooks.select().where(models.Notebooks.uuid == str(kwargs['notebook_uuid']))
			notebook = [n for n in notebook][0]
		except Exception as e:
			notebook = models.Notebooks.create(uuid = str(kwargs['notebook_uuid']))
			notebook.save()

		# print notebook

		# Create thread if not exists
		try:
			thread = models.Threads.select().where(
				(models.Threads.cell_id == kwargs['cell_id']) & (models.Threads.notebook == notebook.id)
			)
			thread = list(thread)[0]
		except Exception as e:
			thread = models.Threads.create(
				cell_id = kwargs['cell_id'],
				notebook = notebook)
			thread.save()
		# load thread comments

		thread_comments = models.Comments\
			.select(models.Comments)\
			.join(models.Threads)\
			.switch()\
			.where((models.Threads.id == thread) & (models.Threads.notebook == thread.notebook.id) )

		thread_comments = [c.to_json() for c in thread_comments]
		json_data = """{"comment_data": [%s]}"""%(','.join(thread_comments))
		
		self.write(json_data)

class CommentUploadHandler(tornado.web.RequestHandler):
	def post(self, **kwargs):
		# print kwargs
		post_comment = self.get_argument('comment')

		# Create notebook object if not exists
		try:
			notebook = models.Notebooks.select().where(models.Notebooks.uuid == str(kwargs['notebook_uuid']))
			notebook = [n for n in notebook][0]
		except Exception as e:
			notebook = models.Notebooks.create(uuid = str(kwargs['notebook_uuid']))
			notebook.save()

		# print notebook

		# Create thread if not exists
		try:
			thread = models.Threads.select().where(
				(models.Threads.cell_id == kwargs['cell_id']) & (models.Threads.notebook == notebook.id)
			)
			thread = list(thread)[0]
		except Exception as e:
			thread = models.Threads.create(
				cell_id = kwargs['cell_id'],
				notebook = notebook)
			thread.save()

		thread_comments = models.Comments\
			.select(models.Comments)\
			.join(models.Threads)\
			.switch()\
			.where((models.Threads.id == thread) & (models.Threads.notebook == thread.notebook.id) )

		thread_comments = [c.to_json() for c in thread_comments]
		try:
			# Add a new comment
			comment = models.Comments.create(
				username='@HHammond',
				content=post_comment,
				thread=thread,
				location = len(thread_comments)+1
				)
			comment.save()

			# print thread
			self.write("Comments Added Successfully.\n")
			self.write(str(comment.id))
			print "success"
		except Exception as e:
			self.write("Comments failed")

class NonCachedStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')



def scan_notebooks():
	"""TODO: add tree search"""
	global NOTEBOOK_DIR
	print "Scanning notebooks..."
	import utils.filescanner as scanner
	scanner.index_cells(NOTEBOOK_DIR)
	print "Finished scanning."

def convert_notebooks():
	"""Convert notebooks and save in same directory"""
	import utils.convert as c
	global NOTEBOOK_DIR
	print "Converting notebooks..."
	c.convert_dir(NOTEBOOK_DIR)
	print "finished conversions"

def init_app(notebook_dir):

	global NOTEBOOK_DIR, application
	NOTEBOOK_DIR = notebook_dir

	application = tornado.web.Application([
		# Notebooks interactions
		(r'/nb/(?P<notebook_uuid>[0-9]+)/cs/(?P<cell_id>[0-9]+)', CommentHandler),
		(r'/upload/nb/(?P<notebook_uuid>[0-9]+)/cs/(?P<cell_id>[0-9]+)', CommentUploadHandler),
		(r'/notebook/(.*)', NonCachedStaticFileHandler, {'path': NOTEBOOK_DIR}),
		(r'/static/(.*)', NonCachedStaticFileHandler, {'path': os.path.join(base,'static')}),
	])

	# NOTEBOOK_DIR = os.path.join(notebook_dir,'notebooks')

	# initialize models
	Macchiato.datastore.create_tables()

	# Scan notebooks
	scan_notebooks()
	convert_notebooks()

def run():
	print NOTEBOOK_DIR
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8081)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	
	# get notebook folder
	parser = argparse.ArgumentParser()
	parser.add_argument("f", help="Notebooks folder")

	args = parser.parse_args()
	
	init_app(os.path.realpath(args.f))
	run()
