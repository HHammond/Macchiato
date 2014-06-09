import peewee

import models

def create_tables():
    try: models.Notebooks.create_table()
    except: pass
    try: models.Threads.create_table()
    except: pass
    try: models.Comments.create_table()
    except: pass
