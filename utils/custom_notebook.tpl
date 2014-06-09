{%- extends 'custom_basic.tpl' -%}


{%- block header -%}
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8" />
<title>{{resources['metadata']['name']}}</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

<script src="/static/js/FormatViewer.js"></script>

<link rel="stylesheet" href="/static/css/notebook.css">
<link rel="stylesheet" href="/static/css/custom.css">
<link href='http://fonts.googleapis.com/css?family=Kameron:400,700' rel='stylesheet' type='text/css'>

<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">

<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 8px;
}

div#notebook {
  overflow: visible;
  border-top: none;
}

@media print {
  div.cell {
    display: block;
    page-break-inside: avoid;
  } 
  div.output_wrapper { 
    display: block;
    page-break-inside: avoid; 
  }
  div.output { 
    display: block;
    page-break-inside: avoid; 
  }
}
</style>

<!-- Load mathjax -->
<script src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
<!-- MathJax configuration -->
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    tex2jax: {
        inlineMath: [ ['$','$'], ["\\(","\\)"] ],
        displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
        processEscapes: true,
        processEnvironments: true
    },
    // Center justify equations in code and markdown cells. Elsewhere
    // we use CSS to left justify single line equations in code cells.
    displayAlign: 'center',
    "HTML-CSS": {
        styles: {'.MathJax_Display': {"margin": 0}},
        linebreaks: { automatic: true }
    }
});
</script>
<!-- End of mathjax configuration -->

<script>
var file_id = "{{nb['metadata']['uuid']}}"
</script>

</head>
{%- endblock header -%}

{% block body %}
<body>

	<div class='container'>
		<h1 class='cover-heading'>Macchiato Server</h1>
		<p class='lead'>IPython Notebook Viewer</p>
		<hr />
	</div>

  <div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container">
{{ super() }}
    </div>
  </div>
  <hr>
</body>
{%- endblock body %}

{% block footer %}
</html>
{% endblock footer %}
