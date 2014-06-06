import os

base = os.path.dirname(os.path.realpath(__file__))
template = os.path.join(base,'md_cell_list.tpl')

print template

c = get_config()

c.NbConvertApp.notebooks = ['*.ipynb']
c.NbConvertApp.export_format = 'custom'

c.Exporter.template_file = template
c.WriterBase.files = ['notebook.css']