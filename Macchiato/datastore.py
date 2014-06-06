import peewee

import models

def create_tables():
    try: models.Notebook.create_table()
    except: pass
    try: models.Thread.create_table()
    except: pass
    try: models.Comment.create_table()
    except: pass


