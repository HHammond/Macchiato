import peewee as pw
import datastore as ds
import json
import os
database = pw.SqliteDatabase('storage/datastore.db')

class BaseModel(pw.Model):
    class Meta:
        database = database

    def __str__(self):
        r = self.to_dict()
        return str(r)

    def to_dict(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return r

    def to_json(self):
        return json.dumps(self.to_dict())

class Notebooks(BaseModel):
    uuid = pw.CharField()

class Threads(BaseModel):
    cell_id    = pw.IntegerField()
    created_at = pw.CharField(null=True)
    deleted_at = pw.CharField(null=True)
    notebook   = pw.ForeignKeyField(Notebooks, related_name='notebook',null=True)

class Comments(BaseModel):
    """Data object representing a comment on a cell"""
    username   = pw.CharField(null=False)
    content    = pw.TextField(null=True)
    created_at = pw.DateTimeField(null=True)
    updated_at = pw.DateTimeField(null=True)
    deleted_at = pw.DateTimeField(null=True)
    location   = pw.IntegerField(null=False)
    thread     = pw.ForeignKeyField(Threads, related_name='thread')
