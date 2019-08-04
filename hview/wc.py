import os
import re
import subprocess

from hview import tree


def generate_wc_tree(filespec):
    line_counts = wc_count_lines(root=filespec.root, files=filespec.files)
    return build_file_tree(line_counts)


def wc_count_lines(root, files):
    cmd = ['wc', '-l'] + list(files)
    proc = subprocess.Popen(cmd,
                            cwd=root,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(None)
    if proc.returncode != 0:
        raise Exception("Error code {} calling wc -l: {}".format(proc.returncode, stderr))

    # Split into lines, discarding the final 'total' line
    lines = stdout.splitlines()[:-1]
    pattern = re.compile(r'^\s*(?P<lines>\d+)\s+(?P<file>.*)$')
    for line in lines:
        m = pattern.match(line)
        yield {
            'file': m.group('file'),
            'lines': m.group('lines'),
        }


def build_file_tree(line_counts, metric='lines'):
    root = tree.Tree('root')
    for rec in line_counts:
        hierarchy = rec['file'].split(os.sep)
        item = {
            'file': rec['file'],
            'value': rec[metric],
            'name': os.path.basename(rec['file']),
        }
        root.insert_item(hierarchy, item)
    return root.list_transformed()
