import peewee as pw
import datastore as ds

import os

database = pw.SqliteDatabase('storage/datastore.db')

class BaseModel(pw.Model):
	class Meta:
		database = database

class Notebook(BaseModel):
	name = pw.CharField()
	location = pw.CharField()

class Thread(BaseModel):
	cell_id =    	pw.IntegerField()
	cell_hash =  	pw.CharField()
	created_at = 	pw.CharField()
	deleted_at = 	pw.CharField()

	notebook = pw.ForeignKeyField(Notebook, related_name='notebook')

class Comment(BaseModel):
	"""Data object representing a comment on a cell"""
	username =		pw.CharField(null=False)
	content =		pw.TextField(null=True)

	created_at =	pw.DateTimeField(null=True)
	updated_at =	pw.DateTimeField(null=True)
	deleted_at =	pw.DateTimeField(null=True)
	
	location = 		pw.IntegerField(null=False)
	thread = 	pw.ForeignKeyField(Thread, related_name='thread')
