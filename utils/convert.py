from IPython import nbconvert as c
from IPython import nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import Exporter, HTMLExporter, TemplateExporter
import jinja2

import os
import re
def convert_dir(dir):

	base = os.path.dirname(os.path.realpath(__file__))
	template_dir = os.path.join(base)
	template = 'custom_notebook.tpl'
	templateLoader = jinja2.FileSystemLoader( searchpath=template_dir )
	templateEnv = jinja2.Environment( loader=templateLoader )

	config = Config()
	config.NbconvertApp.fileext = 'html'
	config.TemplateExporter.template_file = template

	exporter = TemplateExporter(config=config, extra_loaders=[templateLoader], template=template)
	exporter.template_file = template

	for f in [x for x in os.listdir(dir) if re.match('.*\.ipynb$',x)]:
		f = os.path.join(dir,f)
		out = re.match('^(.+)\.ipynb$',f).group(1) + '.html'
		out = re.sub('\s','_',out)
		print out
		nb = nbformat.current.read(open(f,'rw'),'ipynb')

		html, resources = exporter.from_notebook_node(nb)
		html = html.encode('ascii', 'ignore')
		o = open(out,'w')
		o.write(html)
		o.close()
