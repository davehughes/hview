hview - Hierarchical metric viewer
---
Generates and transforms data into a format viewable by [sunburst-chart](https://github.com/vasturiano/sunburst-chart) and
renders charts with a simple local web server.

Quickstart
---
```
git clone https://github.com/davehughes/hview

cd hview
virtualenv env
source env/bin/activate
pip install -r requirements.txt

python -m hview.cli generate-wc --root . > hierarchy.json
python -m hview.cli serve --data hierarchy.json
```
