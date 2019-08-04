import os
import re
import subprocess

from hview import tree


def generate_wc_tree(filespec):
    line_counts = wc_count_lines(root=filespec.root, files=filespec.files)
    return tree.Tree.build(line_counts, adapter=WCLineCount)


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


class WCLineCount(tree.ItemAdapter):
    value_key = 'lines'

    def label(self, item):
        return os.path.basename(item['file'])

    def hierarchy(self, item):
        return item['file'].split(os.sep)


class WCLineCountFileExt(tree.ItemAdapter):
    value_key = 'lines'

    def label(self, item):
        return os.path.basename(item['file'])

    def hierarchy(self, item):
        splits = item['file'].split(os.sep)
        _, extension = os.path.splitext(item['file'])
        return [extension] + splits
