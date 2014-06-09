from IPython import nbconvert, nbformat

import uuid
import re
import os

def index_cells(dir):
    """
    Index cells in all notebooks in given directory
    """
    def find_notebooks(dir):
        return [x for x in os.listdir(dir) if re.match('.*\.ipynb$',x)]

    def modify_notebook(file,dir):
        file = os.path.join(dir,file)
        nb = nbformat.current.read(open(file,'rw'),'ipynb')

        if not nb['metadata'].get('uuid'):
            nb['metadata']['uuid'] = uuid.uuid1().int

        print nb['metadata']

        # get distinct cell ids
        cell_ids = [x['metadata'].get('cell_id') for x in nb['worksheets'][0]['cells']]
        cell_ids = [int(x) for x in cell_ids if x]

        # set an index for new cells
        i = 10000 if len(cell_ids)==0 else max(cell_ids)+1
            
        # index cells
        for cell in nb['worksheets'][0]['cells']:
            if 'cell_id' not in cell['metadata']:
                cell['metadata']['cell_id'] = i
                i+=1

        # rewrite notebook over old one with new data
        nbformat.current.write(nb, open(file,'w'), 'ipynb')

    map(lambda x: modify_notebook(x,dir), find_notebooks(dir))

if __name__=='__main__':
    index_cells(directory)