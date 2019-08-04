import os
import shutil
import SimpleHTTPServer
import SocketServer
import tempfile

import jinja2


BASIC_HTML_VIEW_TEMPLATE = '''
<html>
    <head>
        <script src="https://unpkg.com/d3"></script>
        <script src="https://unpkg.com/sunburst-chart"></script>
    </head>

    <body>
        <div id="chart"></div>
        <script>
            const color = d3.scaleOrdinal(d3.schemePaired);
            fetch('data.json')
                .then(x => x.json())
                .then(data => {
                    var chart = Sunburst()
                    .data(data)
                    .label('name')
                    .size('value')
                    .color((d, parent) => color(parent ? parent.data.name : null))
                    .tooltipContent((d, node) => `Value: <i>${node.value}</i>`)
                    (document.getElementById("chart"))
                })
                .catch(e => {
                    console.log("Error: " + e);
                });
        </script>
    </body>
</html>
'''


def render_basic_html_view(ctx):
    return jinja2.Template(BASIC_HTML_VIEW_TEMPLATE).render(ctx)


def serve_from_tempdir(datafile, bind='', port=8000):
    tempdir = tempfile.mkdtemp()
    try:
        shutil.copyfile(datafile, os.path.join(tempdir, 'data.json'))
        with open(os.path.join(tempdir, 'index.html'), 'w') as f:
            f.write(render_basic_html_view({}))
        os.chdir(tempdir)

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((bind, port), Handler)
        print("serving at port: {}".format(port))
        httpd.serve_forever()
    finally:
        shutil.rmtree(tempdir)
