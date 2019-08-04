import copy
import os
import pathspec


SPEC_DEFAULT_PATHS = ['.ignore', '.gitignore']


class FileTreeSpec(object):
    def __init__(self,
                 root=None,
                 spec_paths=None,
                 spec_lines=None,
                 spec_mode='gitwildmatch',
                 match_mode='ignore'):
        self.root = root or os.getcwd()
        self.spec_paths = spec_paths or []
        self.spec_lines = spec_lines or []
        self.spec_mode = spec_mode
        self.match_mode = match_mode

    @property
    def files(self):
        ignore = self.match_mode == 'ignore'
        return match_pathspec(self.root, self.pathspec, ignore=ignore)

    @property
    def pathspec(self):
        paths = [os.path.join(self.root, p) for p in self.spec_paths]
        lines = copy.copy(self.spec_lines) if self.spec_lines else []
        for path in paths:
            if not os.path.isfile(path):
                continue
            lines.extend(open(path).read().splitlines())

        # Return pathspec built from merged lines from all ignore files
        return pathspec.PathSpec.from_lines('gitwildmatch', lines)


def match_pathspec(root, spec, ignore=True):
    # To do positive match, we can just use pathspec's match_tree
    if not ignore:
        for match in spec.match_tree(root):
            yield match

    # To do a negative match (i.e. all files but those that match the spec), we
    # need to walk the tree ourselves, since pathspec doesn't provide a way to
    # invert its matches.
    for is_match, path in _generate_walk_matches(root, spec):
        if not is_match:
            yield path


def _generate_walk_matches(root, spec):
    for dir_, dirs, files in os.walk(root):
        for f in files:
            abspath = os.path.join(dir_, f)
            relpath = os.path.relpath(abspath, root)
            yield spec.match_file(relpath), relpath
