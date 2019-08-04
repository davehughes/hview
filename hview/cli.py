import argparse
import json
import os
import sys
import shutil
import SimpleHTTPServer
import SocketServer
import tempfile

import hview.wc
import hview.files


def create_parser():
    main_parser = argparse.ArgumentParser(
        prog='hview',
        description='Hierarchical data viewer and utilities',
    )
    sub = main_parser.add_subparsers()

    # Subcommand to generate tree data using `wc -l`
    p = sub.add_parser('generate-wc')
    add_file_metric_args(p)
    add_outputfile_args(p)
    p.set_defaults(func=cmd_generate_wc)

    # Subcommand to serve the hierarchy via a simple local web server
    p = sub.add_parser('serve')
    p.add_argument('--port', default='8000', type=int)
    p.add_argument('--bind', default='')
    p.add_argument('--data', default='data.json')
    p.set_defaults(func=cmd_serve)

    return main_parser


def add_file_metric_args(p):
    p.add_argument(
        '--ignorefile',
        dest='ignorefiles',
        action='append',
        default=['.ignore', '.gitignore'],
    )
    p.add_argument(
        '--ignore',
        dest='ignores',
        action='append',
    )
    p.add_argument(
        '--root',
        required=True,
    )
    return p


def file_tree_spec_from_args(args):
    return hview.files.FileTreeSpec(
        root=args.root,
        spec_paths=args.ignorefiles,
        spec_lines=args.ignores,
        match_mode='ignore',
    )


def add_outputfile_args(p):
    p.add_argument(
        'outfile',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout,
    )
    return p


def cmd_generate_wc(args):
    filetree_spec = file_tree_spec_from_args(args)
    tree = hview.wc.generate_wc_tree(filetree_spec)
    json.dump(tree, args.outfile)


def cmd_serve(args):
    if not os.path.isfile(args.data):
        print("Invalid data file, exiting...")
        return

    # Copy data and HTML page to tempfile and serve from there
    tempdir = tempfile.mkdtemp()
    try:
        shutil.copyfile(args.data, os.path.join(tempdir, 'data.json'))
        shutil.copyfile('index.html', os.path.join(tempdir, 'index.html'))
        os.chdir(tempdir)

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((args.bind, args.port), Handler)
        print("serving at port: {}".format(args.port))
        httpd.serve_forever()
    finally:
        shutil.rmtree(tempdir)


def main(raw_args=None):
    raw_args = raw_args or sys.argv[1:]
    parser = create_parser()
    args = parser.parse_args(raw_args)
    args.func(args)


if __name__ == '__main__':
    main()
